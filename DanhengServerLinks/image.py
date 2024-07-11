from html2image import Html2Image
from jinja2 import Template
import json

base_html = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Player Profile</title>
    <style>
        @font-face {
            font-family: 'SDK_SC_Web';
            src: url('{{ font_path }}');
        }
        body {
            font-family: SDK_SC_Web;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: transparent;
        }

        .profile-container {
            background: rgba(180, 180, 180, 1);
            padding: 24px;
            border-radius: 12px;
            width: 420px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }

        .avatar {
            width: 96px;
            height: 96px;
            border-radius: 50%;
            background: url('{{ avatar_image }}') no-repeat center center;
            background-size: cover;
            margin-bottom: 24px;
        }

        .name,
        .signature,
        .info-item {
            margin-bottom: 12px;
        }

        .name {
            font-size: 28.8px;
            font-weight: bold;
        }

        .signature {
            font-size: 16.8px;
            color: #555;
        }

        .info-item {
            display: flex;
            align-items: center;
            font-size: 19.2px;
        }

        .info-item img {
            width: 28.8px;
            height: 28.8px;
            margin-right: 9.6px;
        }

        .assists,
        .team {
            display: flex;
            align-items: center;
        }

        .assists img,
        .team img {
            width: 48px;
            margin-left: 11px;
            height: 48px;
            margin-right: 6px;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <div class="profile-container">
        <div class="avatar"></div>
        <div class="name">{{ player_name }}</div>
        <div class="signature">{{ player_signature }}</div>
        <div class="info-item">
            <img src="{{ jade_img_path }}" alt="Jade">
            星琼: {{ jade }}
        </div>
        <div class="info-item">
            <img src="{{ credit_img_path }}" alt="Credit">
            信用点: {{ credit }}
        </div>
        <div class="info-item">
            <img src="{{ stamina_img_path }}" alt="Stamina">
            开拓力: {{ stamina }}
        </div>
        <div class="info-item">
            <img src="{{ reserve_img_path }}" alt="Reserve">
            后备开拓力: {{ reserve }}
        </div>
        <div class="info-item">
            <img src="{{ mainStatusPng }}" alt="Status">
            当前状态: {{ status }}
        </div>
        <div class="info-item">
            <img src="{{ subStatusPng }}" alt="SubStatus">
            正处在: {{ subStatus }}
        </div>
        <div class="info-item assists">
            <img src="{{ friend_icon_path }}" alt="Assist">
            支援角色:  
            <img src="{{ assist_1 }}" alt="Assist 1">
            <img src="{{ assist_2 }}" alt="Assist 2">
            <img src="{{ assist_3 }}" alt="Assist 3">
        </div>
        <div class="info-item team">
            <img src="{{ team_icon_path }}" alt="Team">
            队伍角色:
            <img src="{{ team_1 }}" alt="Team 1">
            <img src="{{ team_2 }}" alt="Team 2">
            <img src="{{ team_3 }}" alt="Team 3">
            <img src="{{ team_4 }}" alt="Team 4">
        </div>
    </div>
</body>
</html>
"""

def write_pic(headIcon:int, name: str, signature: str, status: str, subStatus: str, stamina: int, reserve: int, jade: int, credit: int, assistAvatars: list, curLineupAvatars: list, assest_dir: str = ""):
    template = Template(base_html)
    avatar_json_path = assest_dir + 'cn/avatars.json'
    avatar_json = json.load(open(avatar_json_path, 'r', encoding='utf-8'))
    avatar = avatar_json[str(headIcon)]
    character_json_path = assest_dir + 'cn/characters.json'
    character_json = json.load(open(character_json_path, 'r', encoding='utf-8'))

    assist_1 = character_json.get(str(assistAvatars[0]), {}).get('icon', "icon/character/None.png") if len(assistAvatars) > 0 else "icon/character/None.png"
    assist_2 = character_json.get(str(assistAvatars[1]), {}).get('icon', "icon/character/None.png") if len(assistAvatars) > 1 else "icon/character/None.png"
    assist_3 = character_json.get(str(assistAvatars[2]), {}).get('icon', "icon/character/None.png") if len(assistAvatars) > 2 else "icon/character/None.png"
    
    team_1 = character_json.get(str(curLineupAvatars[0]), {}).get('icon', "icon/character/None.png") if len(curLineupAvatars) > 0 else "icon/character/None.png"
    team_2 = character_json.get(str(curLineupAvatars[1]), {}).get('icon', "icon/character/None.png") if len(curLineupAvatars) > 1 else "icon/character/None.png"
    team_3 = character_json.get(str(curLineupAvatars[2]), {}).get('icon', "icon/character/None.png") if len(curLineupAvatars) > 2 else "icon/character/None.png"
    team_4 = character_json.get(str(curLineupAvatars[3]), {}).get('icon', "icon/character/None.png") if len(curLineupAvatars) > 3 else "icon/character/None.png"

    status_dict = {
        "Offline": ("离线", "icon/sign/QuitIcon.png"),
        "Explore": ("开拓中", "icon/sign/DailyQuestExploreIcon.png"),
        "Rogue": ("模拟宇宙", "icon/sign/QuestRogueIcon.png"),
        "ChessRogue": ("模拟宇宙：寰宇蝗灾", "icon/sign/QuestRogueIcon.png"),
        "ChessRogueNous": ("模拟宇宙：黄金与机械", "icon/sign/QuestRogueIcon.png"),
        "RogueTourn": ("差分宇宙", "icon/sign/QuestRogueIcon.png"),
        "Challenge": ("忘却之庭", "icon/sign/AbyssIcon01.png"),
        "ChallengeStory": ("虚构叙事", "icon/sign/World02Icon.png"),
        "ChallengeBoss": ("末日幻影", "icon/sign/World00Icon.png"),
        "Raid": ("任务场景", "icon/sign/QuestIcon.png"),
        "StoryLine": ("故事线", "icon/sign/QuestMainIcon.png"),
        "Activity": ("活动", "icon/sign/ActivityIcon.png")
    }
    sub_status_dict = {
        "Battle": ("战斗中", "icon/sign/MazeSkillIcon.png"),
        "None": ("无", "icon/sign/AllIcon.png")
    }

    status, status_img = status_dict.get(status, ("未知", "icon/sign/AllIcon.png"))
    subStatus, subStatus_img = sub_status_dict.get(subStatus, ("未知", "icon/sign/AllIcon.png"))
    html_content = template.render(
        font_path=assest_dir + 'font/SDK_SC_Web.ttf',
        jade_img_path=assest_dir + 'icon/item/900001.png',
        credit_img_path=assest_dir + 'icon/item/2.png',
        stamina_img_path=assest_dir + 'icon/item/11.png',
        reserve_img_path=assest_dir + 'icon/item/12.png',
        friend_icon_path=assest_dir + 'icon/sign/FriendIcon.png',
        team_icon_path=assest_dir + 'icon/sign/TeamIcon.png',
        avatar_image=assest_dir + avatar['icon'],
        player_name=name,
        player_signature=signature,
        jade=jade,
        credit=credit,
        stamina=stamina,
        reserve=reserve,
        mainStatusPng=assest_dir + status_img,
        status=status,
        subStatusPng=assest_dir + subStatus_img,
        subStatus=subStatus,
        assist_1=assest_dir + assist_1,
        assist_2=assest_dir + assist_2,
        assist_3=assest_dir + assist_3,
        team_1=assest_dir + team_1,
        team_2=assest_dir + team_2,
        team_3=assest_dir + team_3,
        team_4=assest_dir + team_4,
    )
    hti = Html2Image(browser_executable="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
    path_list = hti.screenshot(html_str=html_content, size=(490, 635), save_as="tempOutput.png")
    path = path_list[0]
    return path