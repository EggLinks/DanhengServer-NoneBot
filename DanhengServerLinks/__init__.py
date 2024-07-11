from nonebot import on_command
from .tools import Tools
from .config import Config
from .image import *

from nonebot.params import CommandArg, CommandStart
from pathlib import Path
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot import get_plugin_config
from nonebot.adapters import Event
import json
import nonebot

plugin_config = get_plugin_config(Config)
global_config = nonebot.get_driver().config

tools = Tools(plugin_config.danheng_ip)

def process_message(initial_msg:list) -> Message:
    '''将列表拼接成消息段'''
    messages = []
    for i in initial_msg:
        if i['type'] == 'image':
            messages.append(
                MessageSegment.image(Path(i['path']))
            )
        elif i['type'] == 'text':
            messages.append(
                MessageSegment.text(i['text'])
            )
    return Message(messages)

info = on_command("info", aliases={"信息", "服务器信息"}, priority=10, block=True)
exec = on_command("run", aliases={"执行", "execute"}, priority=10, block=True)
player = on_command("player", aliases={"玩家信息"}, priority=10, block=True)

@exec.handle()
async def exec_handle(bot, 
                      event,
                      args: Message=CommandArg(),
                      command=CommandStart()):
    if (event.get_user_id() not in global_config.superusers):
        await exec.finish("你没有权限这么做！")
    args = str(args).strip()
    if (len(args.split(' ')) < 2):
        await exec.finish('请输入目标uid和指令')
    target = args.split(' ')[0]
    cmd = args.split(' ')[1:]
    exec_result = tools.exec(' '.join(cmd), target, plugin_config.danheng_admin_key)

    await exec.finish(exec_result)

@player.handle()
async def player_handle(bot, 
                      event,
                      args: Message=CommandArg(),
                      command=CommandStart()):
    args = str(args).strip()
    if (len(args.split(' ')) < 1 or args == ''):
        await player.finish('请输入目标uid')
    target = args.split(' ')[0]
    player_result = tools.player_info(target, plugin_config.danheng_admin_key)
    if player_result['code'] != 0:
        await player.finish(player_result['message'])
    path = write_pic(player_result['data']['headIconId'], player_result['data']['name'], player_result['data']['signature'], player_result['data']['playerStatus'], player_result['data']['playerSubStatus'], player_result['data']['stamina'], player_result['data']['recoveryStamina'], player_result['data']['jade'], player_result['data']['credit'], player_result['data']['assistAvatarList'], player_result['data']['lineupBaseAvatarIdList'], plugin_config.danheng_assest_dir)
    dict = [{
        "type": "image",
        "path": path
    }]
    message = process_message(dict)
    await player.finish(message=message)

    
@info.handle()
async def info_handle(bot, 
                      event,
                      args: Message=CommandArg(),
                      command=CommandStart()):
    info_result = tools.info(plugin_config.danheng_admin_key)
    result = "服务器内存：%d MB / %d MB (服务端占用 %d MB)\n在线人数：%d (" % (info_result['data']['usedMemory'], 
                                                             info_result['data']['maxMemory'], 
                                                             info_result['data']['programUsedMemory'], 
                                                             len(info_result['data']['onlinePlayers']))
    for i in info_result['data']['onlinePlayers']:
        result += str(i['uid']) + ', '
    result = result[:-2] + ')'
    await info.finish(result)