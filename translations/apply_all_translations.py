# -*- coding: utf-8 -*-
"""
Master script to apply Vietnamese translations across:
1. chapters/<chapter-dir>/chapter_data.json
2. data/all_chapters.json
3. chapters/<chapter-dir>/chapter_vi.md
4. chapters/<chapter-dir>/chapter_vi_bilingual.md (strictly VI and ZH)
5. chapters/<chapter-dir>/index.html (Offline Reader with Tiếng Việt and 简体中文 only)
6. Root index.html and README.md
"""

import sys, os, json, re, copy, glob, shutil
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))
from bs4 import BeautifulSoup

from translations.trans_ch0 import CHAPTER_0_VI
from translations.trans_ch1 import CHAPTER_1_VI
from translations.trans_ch2_1 import CHAPTER_2_1_VI
from translations.trans_ch2_2 import CHAPTER_2_2_VI
from translations.trans_ch2_3 import CHAPTER_2_3_VI
from translations.trans_ch3_1 import CHAPTER_3_1_VI
from translations.trans_ch3_2 import TRANSLATIONS_CH3_2
from translations.trans_ch4_1 import TRANSLATIONS_CH4_1
from translations.trans_ch4_2 import TRANSLATIONS_CH4_2
from translations.trans_ch5_1 import TRANSLATIONS_CH5_1
from translations.trans_ch5_2 import TRANSLATIONS_CH5_2, SPAN_MAPPINGS_CH5_2

CHAPTER_CONFIGS = [
    {
        'id': 'chapter-0-prologue',
        'dir': 'chapter-0-prologue',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 0: Mở đầu · v5.2.55',
        'title_zh': '云虫 第零章 楔子 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 0: Mở đầu',
        'menu_label': 'Chương 0: Mở đầu',
        'menu_label_zh': '第零章 楔子',
        'trans_panels': CHAPTER_0_VI
    },
    {
        'id': 'chapter-1-xiyang',
        'dir': 'chapter-1-xiyang',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 1: Hi Dương · v5.2.55',
        'title_zh': '云虫 第一章 希扬 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 1: Hi Dương',
        'menu_label': 'Chương 1: Hi Dương',
        'menu_label_zh': '第一章 希扬',
        'trans_panels': CHAPTER_1_VI
    },
    {
        'id': 'chapter-2-cloud-dwellers-1',
        'dir': 'chapter-2-cloud-dwellers-1',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 2: Người Trong Mây · I · v5.2.55',
        'title_zh': '云虫 第二章 云中人 · 一 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 2: Người Trong Mây · I',
        'menu_label': 'Chương 2: Người Trong Mây · I',
        'menu_label_zh': '第二章 云中人 · 一',
        'trans_panels': CHAPTER_2_1_VI
    },
    {
        'id': 'chapter-2-cloud-dwellers-2',
        'dir': 'chapter-2-cloud-dwellers-2',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 2: Người Trong Mây · II · v5.2.55',
        'title_zh': '云虫 第二章 云中人 · 二 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 2: Người Trong Mây · II',
        'menu_label': 'Chương 2: Người Trong Mây · II',
        'menu_label_zh': '第二章 云中人 · 二',
        'trans_panels': CHAPTER_2_2_VI
    },
    {
        'id': 'chapter-2-cloud-dwellers-3',
        'dir': 'chapter-2-cloud-dwellers-3',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 2: Người Trong Mây · III · v5.2.55',
        'title_zh': '云虫 第二章 云中人 · 三 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 2: Người Trong Mây · III',
        'menu_label': 'Chương 2: Người Trong Mây · III',
        'menu_label_zh': '第二章 云中人 · 三',
        'trans_panels': CHAPTER_2_3_VI
    },
    {
        'id': 'chapter-3-beyond-light-cone-1',
        'dir': 'chapter-3-beyond-light-cone-1',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 3: Ngoài Nón Ánh Sáng · I · v5.2.55',
        'title_zh': '云虫 第三章 光锥之外 · 一 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 3: Ngoài Nón Ánh Sáng · I',
        'menu_label': 'Chương 3: Ngoài Nón Ánh Sáng · I',
        'menu_label_zh': '第三章 光锥之外 · 一',
        'trans_panels': CHAPTER_3_1_VI
    },
    {
        'id': 'chapter-3-beyond-light-cone-2',
        'dir': 'chapter-3-beyond-light-cone-2',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 3: Ngoài Nón Ánh Sáng · II · v5.2.55',
        'title_zh': '云虫 第三章 光锥之外 · 二 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 3: Ngoài Nón Ánh Sáng · II',
        'menu_label': 'Chương 3: Ngoài Nón Ánh Sáng · II',
        'menu_label_zh': '第三章 光锥之外 · 二',
        'flat_trans': TRANSLATIONS_CH3_2
    },
    {
        'id': 'chapter-4-fate-1',
        'dir': 'chapter-4-fate-1',
        'arch': 'A',
        'title_vi': 'Vân Trùng · Chương 4: Nón Định Mệnh · I · v5.2.55',
        'title_zh': '云虫 第四章 命运之锥 · 一 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 4: Nón Định Mệnh · I',
        'menu_label': 'Chương 4: Nón Định Mệnh · I',
        'menu_label_zh': '第四章 命运之锥 · 一',
        'flat_trans': TRANSLATIONS_CH4_1
    },
    {
        'id': 'chapter-4-fate-2',
        'dir': 'chapter-4-fate-2',
        'arch': 'B',
        'title_vi': 'Vân Trùng · Chương 4: Nón Định Mệnh · II · v5.2.55',
        'title_zh': '云虫 第四章 命运之锥 · 二 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 4: Nón Định Mệnh · II',
        'menu_label': 'Chương 4: Nón Định Mệnh · II',
        'menu_label_zh': '第四章 命运之锥 · 二',
        'flat_trans': TRANSLATIONS_CH4_2
    },
    {
        'id': 'chapter-5-wuzhui-1',
        'dir': 'chapter-5-wuzhui-1',
        'arch': 'B',
        'title_vi': 'Vân Trùng · Chương 5: Ô Chuy · I · v5.2.55',
        'title_zh': '云虫 第五章 乌骓 · 一 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 5: Ô Chuy · I',
        'menu_label': 'Chương 5: Ô Chuy · I',
        'menu_label_zh': '第五章 乌骓 · 一',
        'flat_trans': TRANSLATIONS_CH5_1
    },
    {
        'id': 'chapter-5-wuzhui-2',
        'dir': 'chapter-5-wuzhui-2',
        'arch': 'B',
        'title_vi': 'Vân Trùng · Chương 5: Ô Chuy · II · v5.2.55',
        'title_zh': '云虫 第五章 乌骓 · 二 · v5.2.55',
        'opening_brand': 'Vân Trùng',
        'opening_title': 'Chương 5: Ô Chuy · II',
        'menu_label': 'Chương 5: Ô Chuy · II',
        'menu_label_zh': '第五章 乌骓 · 二',
        'flat_trans': TRANSLATIONS_CH5_2
    }
]

SPAN_MAPPINGS_CH4_2 = {
    '“也不能算巧合。”': '“Cũng không hẳn là trùng hợp.”',
    '希扬说，': 'Hi Dương nói,',
    '“关于这件事，有两种解释，看你更喜欢哪一种。”': '“Về chuyện này có hai cách giải thích, xem em thích cách nào hơn.”',
    '“第一种，”': '“Cách thứ nhất,”',
    '他把手里的笔在桌上转了一圈，慢慢说道，': 'Cậu xoay xoay cây bút trong tay trên mặt bàn, chậm rãi nói,',
    '“第二种就简单多了。”': '“Cách thứ hai thì đơn giản hơn nhiều.”',
    '希扬的目光落到了她那把白色的贝斯上，': 'Ánh mắt Hi Dương dừng lại trên cây đàn bass màu trắng của cô,',
    '“因为月亮不想让别人看见她的另一面。”': '“Bởi vì mặt trăng không muốn để người khác nhìn thấy mặt còn lại của mình.”',
    '“那太阳和月亮之间，隔了多远？”': '“Vậy giữa mặt trời và mặt trăng, cách nhau bao xa?”',
    '月牙儿像是在想着什么，忽然又问。': 'Nguyệt Nha Nhi dường như đang suy nghĩ điều gì, đột nhiên lại hỏi.',
    '“因为光速，是这个宇宙最底层的法则。”': '“Bởi vì tốc độ ánh sáng là quy luật tầng sâu nhất của vũ trụ này.”',
    '他说，': 'Cậu nói,',
    '“一切有序信息的极限速度，都是光速。只要你还在这个法则之内，就没有任何东西能真正越过它，到达光锥之外。”': '“Tốc độ giới hạn của mọi thông tin có trật tự đều là tốc độ ánh sáng. Chỉ cần em còn ở trong phạm vi quy luật này, thì không có bất cứ thứ gì có thể thực sự vượt qua nó để đến ngoài nón ánh sáng.”',
    '“这条横轴，代表时间。往右是未来，往左是过去。原点——': '“Trục hoành này đại diện cho thời gian. Sang phải là tương lai, sang trái là quá khứ. Gốc tọa độ——',
    '就是现在。”': 'chính là hiện tại.”',
    '“假设你出生的时空位置是原点。”': '“Giả sử vị trí thời - không lúc em sinh ra là gốc tọa độ.”',
    '希扬继续往右，在横轴上取了一个点，': 'Hi Dương tiếp tục dịch sang bên phải, chấm một điểm trên trục thời gian,',
    '“而这里，是时间轴上的一百年后，我们把它叫作A点。然后以这个A点为圆心，在空间平面上画一个半径为一百光年的圆。这个圆，就是你在一百年后理论上能抵达的边界。”': '“Còn đây, là thời điểm một trăm năm sau trên trục thời gian, chúng ta gọi nó là điểm A. Sau đó lấy điểm A này làm tâm, vẽ một hình tròn có bán kính một trăm năm ánh sáng trên mặt phẳng không gian. Hình tròn này, chính là ranh giới trên lý thuyết mà em có thể chạm tới sau một trăm năm.”',
    '“对。”': '“Đúng vậy.”',
    '“再把这个圆和原点连起来，你看它像什么？”': '“Nối hình tròn này lại với gốc tọa độ, em xem nó giống hình gì?”',
    '“这就是属于你的光锥。关于你的一切信息，都只能存在在这个范围之内。因为一切有序信息都不可能超过光速，所以它们永远不可能突破这个光锥之壁。你的存在、你的影响，你能到达的地方，你能让别人知道的事——都被关在这个范围里。对光锥之外的任何一个点来说，关于你的信息都到不了那里，所以从它的角度看，你是不存在的。”': '“Đây chính là nón ánh sáng thuộc về em. Mọi thông tin liên quan đến em đều chỉ có thể tồn tại bên trong phạm vi này. Bởi vì tất cả thông tin có trật tự đều không thể vượt quá vận tốc ánh sáng, cho nên chúng vĩnh viễn không thể đâm xuyên qua bức tường nón ánh sáng này. Sự tồn tại của em, ảnh hưởng của em, những nơi em có thể đặt chân tới, những điều em có thể cho người khác biết——đều bị giam cầm bên trong phạm vi này. Đối với bất kỳ điểm nào nằm ngoài nón ánh sáng, thông tin về em đều không thể truyền tới đó, vì thế dưới góc nhìn của nó, em hoàn toàn không tồn tại.”',
    '“一个囚笼。”': '“Một chiếc lồng giam.”',
    '她轻声道。': 'Cô khẽ lẩm bẩm.',
    '“无序信息。”': '“Thông tin vô trật tự.”',
    '希扬点头，': 'Hi Dương gật đầu,',
    '“你可以先把它理解成一个最简单的量子纠缠模型。”': '“Em có thể hiểu nó như một mô hình vướng víu lượng tử đơn giản nhất.”',
    '“也就是说，”': '“Nói cách khác,”',
    '月牙儿轻声接道，': 'Nguyệt Nha Nhi khẽ tiếp lời,',
    '“这条信息传到了两千年前。”': '“thông tin này đã truyền tới hai nghìn năm trước.”',
    '“这条信息已经越过了光速，到达了光锥之外。”': '“Thông tin này đã vượt qua tốc độ ánh sáng, chạm tới ngoài nón ánh sáng.”',
    '“魔鬼就在这里。因为那是一条无序信息。”': '“Ác quỷ nằm ở chính chỗ này. Bởi vì đó là một thông tin vô trật tự.”',
    '“它虽然同步，但本身是随机的。你和张良谁都不能决定下一次它是正旋还是反旋。我们只能看见它发生了什么，却无法控制它发生什么。”': '“Tuy rằng nó đồng bộ, nhưng bản thân nó lại là ngẫu nhiên. Cả em lẫn Trương Lương đều không thể quyết định lần tiếp theo nó sẽ xoay thuận hay xoay nghịch. Chúng ta chỉ có thể nhìn thấy điều gì đã xảy ra, chứ không thể kiểm soát được điều gì sẽ xảy ra.”',
    '“因为那个时候，他还不是商鞅，只是公孙鞅。是在后来变法成功、被封到商地之后，他才有了‘商鞅’这个名字。你那一句话，对他来说就是一条来自后世的有序信息。那已经不是普通的交谈了，而是在改动他对自己命运的认知。这样的信息一旦出口，通道就会立刻中断。”': '“Bởi vì vào thời điểm đó, ông ấy vẫn chưa phải là Thương Ưởng, mà chỉ là Công Tôn Ưởng. Phải đến sau này biến pháp thành công, được phong đất ở đất Thương, ông ấy mới có cái tên ‘Thương Ưởng’. Một câu nói đó của em, đối với ông ấy chính là một thông tin có trật tự đến từ hậu thế. Đó đã không còn là cuộc trò chuyện thông thường nữa, mà là đang làm thay đổi nhận thức của ông ấy về số phận của chính mình. Loại thông tin như thế một khi thốt ra, thông đạo sẽ lập tức bị gián đoạn.”',
    '“在西藏。”': '“Ở Tây Tạng.”',
    '月牙儿低声说，': 'Nguyệt Nha Nhi trầm giọng nói,',
    '“那次我去追盘古云虫的时候。”': '“Lần đó tôi đi đuổi theo Vân Trùng Bàn Cổ.”',
    '“张良那天说，我们在光锥之外。”': '“Trương Lương ngày hôm đó từng nói, chúng ta đang ở ngoài nón ánh sáng.”',
    '她看着他，': 'Cô nhìn cậu,',
    '“这到底是什么意思？什么叫光锥？光锥之外又是什么地方？”': '“Rốt cuộc câu đó có ý nghĩa gì? Thế nào gọi là nón ánh sáng? Ngoài nón ánh sáng lại là nơi chốn thế nào?”',
    '“好。”': '“Được.”',
    '月牙儿说，': 'Nguyệt Nha Nhi nói,',
    '“时空坐标。”': '“Tọa độ thời - không.”',
    '云虫': 'Vân Trùng',
    '第四章 命运之锥': 'Chương 4: Nón Định Mệnh'
}

SPAN_MAPPINGS_CH5_1 = {
    '[云虫]': '[Vân Trùng]',
    '7115恒星系7号文明第6次审判记事': 'Biên niên sử phán xét lần thứ 6 của nền văn minh số 7 thuộc hệ sao 7115',
    '仅记录与审判相关内容': 'Chỉ ghi chép các nội dung liên quan đến cuộc phán xét',
    '“乌江。”': '“Ô Giang.”',
    '他说，': 'Chàng nói,',
    '“我们在这儿接一个人。”': '“Chúng ta ở đây để đón một người.”',
    '“那……他不会上船的。”': '“Thế nhưng…… ông ấy sẽ không lên thuyền đâu.”',
    '月牙儿不假思索地接了一句。': 'Nguyệt Nha Nhi buột miệng nói theo bản năng.',
    '“你怎么知道？”': '“Sao anh lại biết?”',
    '月牙儿问。': 'Nguyệt Nha Nhi hỏi.',
    '“……云中人？”': '“……Người trong mây?”',
    '月牙儿皱起眉头。': 'Nguyệt Nha Nhi nhíu mày.',
    '“当年，籍与八千江东子弟渡江而西。”': '“Năm xưa, Tịch này cùng tám ngàn con em Giang Đông vượt sông sang phía tây.”',
    '他望着江水，声音不高，': 'Ông nhìn dòng nước cuộn chảy, giọng trầm buồn,',
    '“今日，归者无一。”': '“Ngày nay, chẳng một ai trở về.”',
    '“纵使他们不怪罪，”': '“Dẫu cho họ không trách cứ,”',
    '“我又岂能问心无愧？”': '“nhưng lòng ta há có thể không thẹn với lương tâm?”',
    '“项王，恕臣直言。”': '“Hạng Vương, thứ cho thần nói thẳng.”',
    '“大王自万军之中冒死杀至此处，求的，不就是一线生机么？如今船在眼前，江东在对岸。为何偏偏不肯上船？”': '“Đại Vương từ trong muôn trùng vây hãm liều chết xông tới tận đây, cầu mong chẳng phải là một tia hy vọng sống sót sao? Nay thuyền ở ngay trước mắt, Giang Đông ở bờ bên kia. Vì cớ gì lại nhất quyết không chịu lên thuyền?”',
    '“吾自阴陵迷道，”': '“Ta từ Âm Lăng lạc bước lầm đường,”',
    '他缓缓道，': 'Ông chậm rãi nói,',
    '“田父绐我，陷于大泽。大雾锁江，芦苇没人，断断续续，不辨南北，连走到了乌江哪一段，亦不自知。”': '“bị lão nông lừa gạt, sa vào chốn đầm lầy lớn. Sương mù dày đặc vây kín sông, lau sậy cao ngập đầu người, quanh co đứt đoạn, chẳng phân biệt nổi bắc nam, đến mức đi tới khúc nào của Ô Giang này, bản thân ta cũng chẳng hề hay biết.”',
    '“籍，亦非愚钝之人。”': '“Tịch này, há phải là kẻ ngu đần mông muội.”',
    '他道，': 'Ông nói,',
    '“这乌江之上，何来的亭长？又何来的渡船？”': '“Khúc Ô Giang hoang vu này, làm gì có đình trưởng nào? Lại làm gì có thuyền đò nào?”',
    '西楚霸王': 'TÂY SỞ BÁ VƯƠNG',
    '项羽': 'Hạng Vũ',
    '名籍 · 字羽': 'Tên Tịch · Tự Vũ',
    '秦末名将，巨鹿之战击破秦军主力。秦亡后号西楚霸王，与刘邦争夺天下，最终兵败垓下，自刎乌江。': 'Danh tướng cuối thời Tần, trong trận Cự Lộc đã đánh tan đại quân chủ lực nhà Tần. Sau khi nhà Tần diệt vong, tự xưng Tây Sở Bá Vương, tranh đoạt thiên hạ cùng Lưu Bang, cuối cùng bại trận tại Cai Hạ, tự vẫn bên bờ Ô Giang.',
    '云虫': 'Vân Trùng',
    '第五章 乌骓': 'Chương 5: Ô Chuy'
}

FOREIGN_LANG_SUFFIXES = ['-en', '-ar', '-es', '-fr', '-ja', '-ko', '-pt-br', '-ru', '-zh-hant']
FOREIGN_ATTR_EXACT = ['data-en', 'data-ar', 'data-es', 'data-fr', 'data-ja', 'data-ko', 'data-pt-br', 'data-ru', 'data-zh-hant', 'data-ptbr']

def strip_foreign_attributes(soup):
    for el in soup.find_all(True):
        attrs_to_remove = []
        for attr in list(el.attrs.keys()):
            if attr in FOREIGN_ATTR_EXACT or any(attr.endswith(sfx) for sfx in FOREIGN_LANG_SUFFIXES):
                attrs_to_remove.append(attr)
        for attr in attrs_to_remove:
            del el[attr]

def resolve_chapter_vi_panels(cfg, data):
    """Return list of lists of VI strings, one per panel."""
    if 'trans_panels' in cfg:
        return cfg['trans_panels']
    elif 'flat_trans' in cfg:
        res = []
        idx = 0
        for p in data['panels']:
            cnt = len(p['texts'].get('zh', []))
            res.append(cfg['flat_trans'][idx:idx+cnt])
            idx += cnt
        return res
    raise ValueError(f"No translation found for {cfg['id']}")

def step1_update_json(all_chapters_data):
    print("=== Step 1: Updating chapter_data.json and collecting master data ===")
    for cfg in CHAPTER_CONFIGS:
        json_path = os.path.join('chapters', cfg['dir'], 'chapter_data.json')
        data = json.load(open(json_path, encoding='utf-8'))
        vi_panels = resolve_chapter_vi_panels(cfg, data)
        
        # Strictly keep only zh and vi
        data['available_languages'] = ['zh', 'vi']
        data['title_vi'] = cfg['title_vi']
        
        for p, vi_list in zip(data['panels'], vi_panels):
            zh_texts = p.get('texts', {}).get('zh', [])
            p['texts'] = {
                'zh': zh_texts,
                'vi': vi_list
            }
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Updated {json_path} (languages: {data['available_languages']}, texts: {sum(len(v) for v in vi_panels)}).")
        all_chapters_data.append(data)
        
    master_path = os.path.join('data', 'all_chapters.json')
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(all_chapters_data, f, ensure_ascii=False, indent=2)
    print(f"  Master {master_path} updated.")

def step2_generate_markdown():
    print("=== Step 2: Generating chapter_vi.md and chapter_vi_bilingual.md (pruning obsolete) ===")
    for cfg in CHAPTER_CONFIGS:
        ch_dir = os.path.join('chapters', cfg['dir'])
        
        # Delete obsolete files
        for obsolete in ['chapter_en.md', 'chapter_bilingual.md']:
            obs_path = os.path.join(ch_dir, obsolete)
            if os.path.exists(obs_path):
                os.remove(obs_path)
                print(f"  Removed obsolete file: {obs_path}")
                
        json_path = os.path.join(ch_dir, 'chapter_data.json')
        data = json.load(open(json_path, encoding='utf-8'))
        
        # 1. Pure VI Markdown
        vi_lines = [
            f"# {cfg['opening_brand']} - {cfg['opening_title']}",
            "",
            "---",
            ""
        ]
        
        # 2. Pure Bilingual VI-ZH Markdown
        bi_lines = [
            f"# {cfg['opening_brand']} / 云虫 - {cfg['opening_title']} ({data.get('title_zh', '')})",
            "",
            "---",
            ""
        ]
        
        for i, p in enumerate(data['panels']):
            p_idx = p.get('panel_index', i + 1)
            img_src = p.get('image_src')
            vid_src = p.get('video_src')
            
            media_md = ""
            if vid_src and not img_src:
                media_md = f'<video controls width="100%" src="./{vid_src}"></video>\n'
            elif vid_src and img_src:
                media_md = f'![Panel {p_idx}](./{img_src})\n\n*(Xem video chuyển động: [`{os.path.basename(vid_src)}`](./{vid_src}))*\n'
            elif img_src:
                media_md = f'![Panel {p_idx}](./{img_src})\n'
            
            if media_md:
                vi_lines.append(media_md)
                bi_lines.append(media_md)
                
            vi_texts = p['texts'].get('vi', [])
            zh_texts = p['texts'].get('zh', [])
            
            for vt in vi_texts:
                vi_lines.append(f"{vt}\n")
                
            max_t = max(len(vi_texts), len(zh_texts))
            for t_idx in range(max_t):
                vt = vi_texts[t_idx] if t_idx < len(vi_texts) else ""
                zt = zh_texts[t_idx] if t_idx < len(zh_texts) else ""
                
                if vt:
                    bi_lines.append(f"**VI**: {vt}\n")
                if zt:
                    bi_lines.append(f"**ZH**: {zt}\n")
                bi_lines.append("\n")
                
            vi_lines.append("\n")
            
        vi_path = os.path.join(ch_dir, 'chapter_vi.md')
        bi_path = os.path.join(ch_dir, 'chapter_vi_bilingual.md')
        
        with open(vi_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(vi_lines).strip() + "\n")
            
        with open(bi_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(bi_lines).strip() + "\n")
            
        print(f"  Generated {vi_path} and {bi_path}")

VI_CSS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,600;0,700;0,800;1,400;1,700;1,800&display=swap" rel="stylesheet">
<style data-cloudinsect-vi-style="true">
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-400-normal.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-400-italic.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-600-normal.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: italic;
  font-weight: 600;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-700-italic.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-700-normal.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: italic;
  font-weight: 700;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-700-italic.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-800-normal.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: italic;
  font-weight: 800;
  font-display: swap;
  src: url('../../assets/fonts/be-vietnam-pro-700-italic.ttf') format('truetype');
}

html[lang="vi"],
html[lang="vi"] body,
html[lang="vi"] * {
  font-family: "Be Vietnam Pro", "Segoe UI", Roboto, -apple-system, BlinkMacSystemFont, Arial, sans-serif !important;
}

html[lang="vi"] .history-card,
html[lang="vi"] .history-card *,
html[lang="vi"] .history-card-kicker,
html[lang="vi"] .history-card-name,
html[lang="vi"] .history-card-courtesy,
html[lang="vi"] .history-card-detail,
html[lang="vi"] .history-card-detail p {
  font-family: "Be Vietnam Pro", "Segoe UI", Roboto, -apple-system, BlinkMacSystemFont, Arial, sans-serif !important;
}

html[lang="vi"] .history-card-kicker {
  font-weight: 700;
  letter-spacing: 0.08em;
}

html[lang="vi"] .history-card-name {
  font-weight: 800;
  letter-spacing: -0.01em;
}

html[lang="vi"] .history-card-courtesy {
  font-weight: 600;
  letter-spacing: 0.02em;
}

html[lang="vi"] .history-card-detail p {
  font-weight: 500;
  line-height: 1.65;
}

html[lang="vi"] .opening-brand {
  line-height: 1.18;
  font-weight: 800;
  letter-spacing: -0.01em;
}

html[lang="vi"] .opening-title {
  line-height: 1.32;
  font-weight: 800;
  letter-spacing: -0.01em;
}

html[lang="vi"] .opening-time {
  line-height: 1.5;
  font-weight: 600;
}

html[lang="vi"] .text {
  font-size: clamp(calc(19px * var(--reader-scale)), calc(1.5vw * var(--reader-scale)), calc(27px * var(--reader-scale)));
  line-height: 1.68;
  font-weight: 600;
  letter-spacing: 0.005em;
}

html[lang="vi"] .quote {
  line-height: 1.6;
  font-weight: 500;
  font-style: italic;
}

html[lang="vi"] .sound-effect {
  line-height: 1.35;
  font-weight: 800;
  font-style: italic;
}

html[lang="vi"] main[data-lang-page="vi"] {
  direction: ltr;
}
</style>
"""

VI_SURFACE_SCRIPT = """<script data-cloudinsect-vi-surface="true">
(function () {
  function applyVietnameseSurface() {
    if ((document.documentElement.lang || '').toLowerCase() !== 'vi') return;
    document.querySelectorAll('[aria-label="Language selection"]').forEach((item) => { item.setAttribute('aria-label', 'Chọn ngôn ngữ'); });
    document.querySelectorAll('.language-select').forEach((item) => { item.setAttribute('aria-label', 'Ngôn ngữ'); });
    document.querySelectorAll('[aria-label="Font size controls"]').forEach((item) => { item.setAttribute('aria-label', 'Cỡ chữ'); });
    document.querySelectorAll('[aria-label="Decrease font size"]').forEach((item) => { item.setAttribute('aria-label', 'Giảm cỡ chữ'); });
    document.querySelectorAll('[aria-label="Increase font size"]').forEach((item) => { item.setAttribute('aria-label', 'Tăng cỡ chữ'); });
    document.querySelectorAll('[aria-label="Reader settings"]').forEach((item) => { item.setAttribute('aria-label', 'Cài đặt đọc'); });
    document.querySelectorAll('[aria-label="Back"]').forEach((item) => { item.setAttribute('aria-label', 'Quay lại'); });
    document.querySelectorAll('[aria-label="动态壁纸列表"]').forEach((item) => { item.setAttribute('aria-label', 'Danh sách hình nền'); });
    document.querySelectorAll('.toc-link').forEach((item) => {
      item.setAttribute('aria-label', 'Quay lại mục lục chính');
      item.setAttribute('title', 'Quay lại mục lục chính');
    });
    document.querySelectorAll('.chapter-pager-button[title="上一节"], [data-pager-disabled="previous"]').forEach((item) => {
      item.setAttribute('title', 'Chương trước');
      item.setAttribute('aria-label', 'Chương trước');
    });
    document.querySelectorAll('.chapter-pager-button[title="下一节"], [data-pager-disabled="next"]').forEach((item) => {
      item.setAttribute('title', 'Chương tiếp theo');
      item.setAttribute('aria-label', 'Chương tiếp theo');
    });
    document.querySelectorAll('summary[title="点击查看人物简介"]').forEach((item) => {
      item.setAttribute('title', 'Nhấn để xem tiểu sử nhân vật');
    });
    const wallpaper = document.querySelector('.wallpaper-entry');
    if (wallpaper) wallpaper.setAttribute('aria-label', 'Hình nền nổi bật');
    const catalog = document.querySelector('.catalog');
    if (catalog) catalog.setAttribute('aria-label', 'Mục lục các chương');
    const chapter = document.querySelector('.chapter-select');
    if (chapter) chapter.setAttribute('aria-label', 'Chọn chương');
    document.querySelectorAll('.chapter-select option').forEach((item) => {
      if (item.dataset.vi) item.textContent = item.dataset.vi;
    });
    const controls = document.querySelector('.chapter-controls');
    if (controls) controls.setAttribute('aria-label', 'Điều hướng chương');
    document.querySelectorAll('[aria-label="章节开场"]').forEach((item) => { item.setAttribute('aria-label', 'Mở đầu chương'); });
    document.querySelectorAll('.cloudinsect-copyright').forEach((item) => { item.textContent = "© WLOP. Toàn bộ nội dung và bản quyền liên quan trên trang web này thuộc về WLOP. Mọi hành vi sao chép, tái bản, cải biên hoặc sử dụng cho mục đích thương mại khi chưa được phép đều bị nghiêm cấm. Bảo lưu mọi quyền."; });
    document.querySelectorAll('.cloudinsect-contact-label').forEach((item) => { item.textContent = "Liên hệ:"; });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', applyVietnameseSurface, { once: true });
  else applyVietnameseSurface();
  window.setTimeout(applyVietnameseSurface, 0);
  const select = document.querySelector('.language-select');
  if (select) select.addEventListener('change', () => setTimeout(applyVietnameseSurface, 0));
}());
</script>
"""

def step3_update_html_readers():
    print("=== Step 3: Updating HTML readers for offline reader (v5.2.55, VI and ZH only) ===")
    for cfg in CHAPTER_CONFIGS:
        html_path = os.path.join('chapters', cfg['dir'], 'index.html')
        content = open(html_path, encoding='utf-8').read()
        
        # Replace legacy version strings in attributes
        content = re.sub(r'v5\.(?:1\.39|2\.54)', 'v5.2.55', content)
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 1. Update version tags
        for el in soup.find_all(class_=['site-version', 'version-badge']):
            el.string = 'v5.2.55'
            
        for el in soup.find_all(attrs={'data-cloudinsect-version': True}):
            el.string = 'v5.2.55'
            
        for meta in soup.find_all('meta', attrs={'name': 'cloudinsect-version'}):
            meta['content'] = 'v5.2.55'
            
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href', '')
            if 'site-footer.css' in href:
                link['href'] = '../../assets/site-footer.css?v=5.2.55'
                
        for sc in soup.find_all('script', src=True):
            src = sc.get('src', '')
            if 'site-footer.js' in src:
                sc['src'] = '../../assets/site-footer.js?v=5.2.55'
                
        # 2. Clean language-select to strictly vi and zh
        for sel in soup.find_all('select', class_='language-select'):
            sel.clear()
            opt_vi = soup.new_tag('option', value='vi')
            opt_vi.string = 'Tiếng Việt'
            opt_zh = soup.new_tag('option', value='zh')
            opt_zh.string = '简体中文'
            sel.append(opt_vi)
            sel.append(opt_zh)
            
        # 3. Clean chapter-select options
        for sel in soup.find_all('select', class_='chapter-select'):
            sel['aria-label'] = 'Chọn chương'
            sel.clear()
            for ch_cfg in CHAPTER_CONFIGS:
                val = f"../{ch_cfg['dir']}/index.html"
                opt = soup.new_tag('option', **{
                    'value': val,
                    'data-vi': ch_cfg['menu_label'],
                    'data-zh': ch_cfg['menu_label_zh']
                })
                if ch_cfg['id'] == cfg['id']:
                    opt['selected'] = ''
                opt.string = ch_cfg['menu_label']
                sel.append(opt)

        for tl in soup.find_all('a', class_='toc-link'):
            tl['aria-label'] = 'Quay lại mục lục chính'
            tl['title'] = 'Quay lại mục lục chính'
                
        # 4. Remove foreign surface scripts
        for sc in soup.find_all('script'):
            for a in list(sc.attrs.keys()):
                if any(x in a for x in ['spanish-surface', 'arabic-surface', 'french-surface', 'ptbr-surface', 'ru-surface']):
                    sc.decompose()
                    break

        # Remove old injected styles and scripts
        for st in soup.find_all('style', attrs={'data-cloudinsect-vi-style': True}):
            st.decompose()
        for sc in soup.find_all('script', attrs={'data-cloudinsect-vi-surface': True}):
            sc.decompose()
        for lk in soup.find_all('link'):
            href = lk.get('href', '')
            if 'fonts.googleapis.com' in href or 'fonts.gstatic.com' in href:
                lk.decompose()

        # 5. Architecture specific handling
        if cfg['arch'] == 'A':
            # Remove all mains other than zh and vi
            for m in soup.find_all('main', class_='comic'):
                lp = m.get('data-lang-page')
                if lp not in ['zh', 'vi']:
                    m.decompose()
                    
            # Recreate vi_main from zh_main
            old_vi_main = soup.find('main', attrs={'data-lang-page': 'vi'})
            if old_vi_main:
                old_vi_main.decompose()
                
            zh_main = soup.find('main', attrs={'data-lang-page': 'zh'})
            if zh_main:
                vi_main = copy.deepcopy(zh_main)
                vi_main['data-lang-page'] = 'vi'
                if vi_main.has_attr('hidden'):
                    del vi_main['hidden']
                zh_main['hidden'] = ''
                
                brand_el = vi_main.find(class_='opening-brand')
                if brand_el: brand_el.string = cfg['opening_brand']
                title_el = vi_main.find(class_='opening-title')
                if title_el: title_el.string = cfg['opening_title']
                for sec in vi_main.find_all('section'):
                    if sec.get('aria-label') == '章节开场':
                        sec['aria-label'] = 'Mở đầu chương'
                        
                for tag in vi_main.find_all(class_=['tag', 'tag-spacer']):
                    if '[云虫]' in tag.get_text():
                        tag.string = '[Vân Trùng]'
                for body in vi_main.find_all(class_='tag-body'):
                    t = body.get_text()
                    if '7115恒星系7号文明第6次审判记事' in t:
                        body.string = 'Biên niên sử phán xét lần thứ 6 của nền văn minh số 7 thuộc hệ sao 7115'
                    elif '仅记录与审判相关内容' in t:
                        body.string = 'Chỉ ghi chép các nội dung liên quan đến cuộc phán xét'
                for op_time in vi_main.find_all(class_='opening-time'):
                    for child in list(op_time.children):
                        if isinstance(child, str) and '距第一次云中行走' in child:
                            child.replace_with(' Ba ngày sau chuyến đi dạo đầu tiên giữa những tầng mây')

                for card in vi_main.find_all('details', class_='history-card'):
                    person = card.get('data-history-person')
                    summary = card.find('summary')
                    if summary:
                        summary['title'] = 'Nhấn để xem tiểu sử nhân vật'
                    if person == 'shang-yang':
                        kicker = card.find(class_='history-card-kicker')
                        if kicker: kicker.string = 'Thời Chiến Quốc · Thương Quân'
                        name = card.find(class_='history-card-name')
                        if name: name.string = 'Thương Ưởng'
                        courtesy = card.find(class_='history-card-courtesy')
                        if courtesy: courtesy.string = 'Tên gốc là Công Tôn Ưởng'
                        detail_p = card.find(class_='history-card-detail')
                        if detail_p and detail_p.find('p'):
                            detail_p.find('p').string = 'Nhà chính trị, cải cách thời Chiến Quốc. Sang Tần phò tá Tần Hiếu Công thực hiện biến pháp, giúp nước Tần lớn mạnh vượt bậc; sau được phong đất ở đất Thương, người đời gọi là Thương Ưởng.'
                    elif person == 'zhang-liang':
                        kicker = card.find(class_='history-card-kicker')
                        if kicker: kicker.string = 'Thời Hán · Lưu Hầu'
                        name = card.find(class_='history-card-name')
                        if name: name.string = 'Trương Lương'
                        courtesy = card.find(class_='history-card-courtesy')
                        if courtesy: courtesy.string = 'Tự Tử Phòng'
                        detail_p = card.find(class_='history-card-detail')
                        if detail_p and detail_p.find('p'):
                            detail_p.find('p').string = 'Mưu thần cuối thời Tần đầu thời Hán, từng mưu sát vua Tần ở Bác Lãng Sa. Sau phò tá Lưu Bang bình định thiên hạ, cùng Tiêu Hà, Hàn Tín được xưng là "Hán Sơ Tam Kiệt", được phong Lưu Hầu.'

                for pager_btn in vi_main.find_all(class_='chapter-pager-button'):
                    if pager_btn.get('title') == '上一节':
                        pager_btn['title'] = 'Chương trước'
                        pager_btn['aria-label'] = 'Chương trước'
                    elif pager_btn.get('title') == '下一节':
                        pager_btn['title'] = 'Chương tiếp theo'
                        pager_btn['aria-label'] = 'Chương tiếp theo'
                        
                json_path = os.path.join('chapters', cfg['dir'], 'chapter_data.json')
                ch_data = json.load(open(json_path, encoding='utf-8'))
                all_vi = []
                for p in ch_data['panels']:
                    all_vi.extend(p.get('texts', {}).get('vi', []))
                    
                p_nodes = vi_main.find_all('p', class_='text')
                has_header_quote = (len(p_nodes) == len(all_vi) + 1)
                if has_header_quote:
                    p_nodes[0].clear()
                    tag_span = soup.new_tag('span', **{'class': 'tag'})
                    tag_span.string = '[Vân Trùng]'
                    p_nodes[0].append(tag_span)
                    p_nodes[0].append(' 7115 hệ sao - Ký sự phán quyết lần thứ 6 của nền văn minh số 7')
                    target_nodes = p_nodes[1:]
                else:
                    target_nodes = p_nodes
                    
                for i, p_node in enumerate(target_nodes):
                    if i < len(all_vi):
                        vi_text = all_vi[i]
                        m_tag = re.match(r'^(\[[^\]]+\])\s*(.*)$', vi_text)
                        if m_tag:
                            tag_part = m_tag.group(1)
                            rest_part = m_tag.group(2)
                            tag_span = soup.new_tag('span', **{'class': 'tag'})
                            tag_span.string = tag_part
                            p_node.clear()
                            p_node.append(tag_span)
                            p_node.append(' ' + rest_part)
                        else:
                            p_node.string = vi_text
                            
                zh_main.insert_after(vi_main)
                
        elif cfg['arch'] == 'B':
            # Architecture B
            main_el = soup.find('main', class_='comic')
            if cfg['id'] == 'chapter-4-fate-2':
                span_map = SPAN_MAPPINGS_CH4_2
            elif cfg['id'] == 'chapter-5-wuzhui-1':
                span_map = SPAN_MAPPINGS_CH5_1
            elif cfg['id'] == 'chapter-5-wuzhui-2':
                span_map = SPAN_MAPPINGS_CH5_2
            else:
                span_map = {}
                
            json_path = os.path.join('chapters', cfg['dir'], 'chapter_data.json')
            ch_data = json.load(open(json_path, encoding='utf-8'))
            all_vi = []
            for p in ch_data['panels']:
                all_vi.extend(p['texts'].get('vi', []))
            all_zh = []
            for p in ch_data['panels']:
                all_zh.extend(p['texts'].get('zh', []))
            zh_to_vi = {z.strip(): v.strip() for z, v in zip(all_zh, all_vi)}
            
            targets = main_el.find_all(lambda el: el.has_attr('data-zh')) if main_el else []
            for t in targets:
                zh_val = t.get('data-zh', '').strip()
                if not zh_val:
                    continue
                vi_val = span_map.get(zh_val)
                if not vi_val:
                    vi_val = zh_to_vi.get(zh_val)
                if vi_val:
                    t['data-vi'] = vi_val
                    t.string = vi_val
                else:
                    t['data-vi'] = zh_val
                    
            if main_el:
                ob = main_el.find(class_='opening-brand')
                if ob and ob.has_attr('data-zh'):
                    ob['data-vi'] = cfg['opening_brand']
                    ob.string = cfg['opening_brand']
                ot = main_el.find(class_='opening-title')
                if ot and ot.has_attr('data-zh'):
                    ot['data-vi'] = cfg['opening_title']
                    ot.string = cfg['opening_title']
                    
            for sm in soup.find_all('summary'):
                if sm.get('title') == '点击查看人物简介':
                    sm['title'] = 'Nhấn để xem tiểu sử nhân vật'
                    
            for sec in soup.find_all('section', class_='chapter-teaser'):
                sec['data-i18n-aria-label-vi'] = 'Dự báo chương tiếp theo'

        # Chapter 5-1 next button & video cleanup
        if cfg['id'] == 'chapter-5-wuzhui-1':
            next_btn = soup.find('span', class_='chapter-pager-button', attrs={'data-pager-disabled': 'next'})
            if next_btn:
                new_a = soup.new_tag('a', **{
                    'class': 'chapter-pager-button',
                    'href': '../chapter-5-wuzhui-2/index.html',
                    'title': 'Chương tiếp theo',
                    'aria-label': 'Chương tiếp theo'
                })
                new_img = soup.new_tag('img', **{
                    'class': 'chapter-pager-icon',
                    'src': '../../assets/pager-next.png',
                    'alt': ''
                })
                new_a.append(new_img)
                next_btn.replace_with(new_a)
                
            next_card = soup.find('a', class_='next-chapter')
            if next_card:
                next_card['href'] = '../chapter-5-wuzhui-2/index.html'

        # Set title
        if soup.title:
            soup.title.string = cfg['title_vi']

        # STRIP ALL FOREIGN ATTRIBUTES (data-en, data-ar, data-es, etc.)
        strip_foreign_attributes(soup)

        html_str = str(soup)
        
        # 6. Update scripts: languageMeta and applyLanguage
        t_vi = cfg['title_vi']
        t_zh = cfg['title_zh']
        
        # Replace languageMeta completely using DOTALL
        new_meta = f'const languageMeta = {{"vi": {{"htmlLang": "vi", "title": "{t_vi}"}}, "zh": {{"htmlLang": "zh-CN", "title": "{t_zh}"}}}};'
        html_str = re.sub(r'const languageMeta = \{[\s\S]*?\};', new_meta, html_str, count=1)
        
        # Replace targets query selector in Arch B
        if cfg['arch'] == 'B':
            html_str = html_str.replace("document.querySelectorAll('[data-zh][data-zh-hant]')", "document.querySelectorAll('[data-zh]')")
            
        # Replace applyLanguage
        if cfg['arch'] == 'A':
            new_apply = """function applyLanguage(nextLang) {
    const anchor = captureReadingAnchor();
    lang = languageMeta[nextLang] ? nextLang : 'zh';
    document.documentElement.lang = languageMeta[lang].htmlLang;
    document.title = languageMeta[lang].title;
    document.querySelectorAll('main[data-lang-page]').forEach((m) => {
      m.hidden = m.getAttribute('data-lang-page') !== lang;
    });
    document.querySelectorAll('.chapter-select option').forEach((opt) => {
      opt.textContent = (lang === 'vi' ? opt.dataset.vi : opt.dataset.zh) || opt.dataset.zh || '';
    });
    document.querySelectorAll('.chapter-select').forEach((sel) => {
      sel.setAttribute('aria-label', lang === 'vi' ? 'Chọn chương' : '选择章节');
    });
    document.querySelectorAll('.toc-link').forEach((link) => {
      const t = lang === 'vi' ? 'Quay lại mục lục chính' : '返回主目录';
      link.setAttribute('aria-label', t);
      link.setAttribute('title', t);
    });
    const langSelect = document.querySelector('.language-select');
    if (langSelect && langSelect.value !== lang) { langSelect.value = lang; }
    writeStoredValue('cloudinsect-lang', lang);
    restoreReadingAnchor(anchor);
    window.dispatchEvent(new Event('resize'));
  }"""
            html_str = re.sub(r'function applyLanguage\(nextLang\) \{[\s\S]*?restoreReadingAnchor\(anchor\);\s*\}', new_apply, html_str, count=1)
        else:
            new_apply = """function applyLanguage(nextLang) {
    const anchor = captureReadingAnchor();
    lang = languageMeta[nextLang] ? nextLang : 'zh';
    document.documentElement.lang = languageMeta[lang].htmlLang;
    document.title = languageMeta[lang].title;
    targets.forEach((el) => {
      el.textContent = (lang === 'vi' ? el.dataset.vi : el.dataset.zh) || el.dataset.zh || '';
    });
    document.querySelectorAll('.chapter-select option').forEach((opt) => {
      opt.textContent = (lang === 'vi' ? opt.dataset.vi : opt.dataset.zh) || opt.dataset.zh || '';
    });
    document.querySelectorAll('.chapter-select').forEach((sel) => {
      sel.setAttribute('aria-label', lang === 'vi' ? 'Chọn chương' : '选择章节');
    });
    document.querySelectorAll('.toc-link').forEach((link) => {
      const t = lang === 'vi' ? 'Quay lại mục lục chính' : '返回主目录';
      link.setAttribute('aria-label', t);
      link.setAttribute('title', t);
    });
    const langSelect = document.querySelector('.language-select');
    if (langSelect && langSelect.value !== lang) { langSelect.value = lang; }
    writeStoredValue('cloudinsect-lang', lang);
    restoreReadingAnchor(anchor);
    window.dispatchEvent(new Event('resize'));
  }"""
            html_str = re.sub(r'function applyLanguage\(nextLang\) \{[\s\S]*?restoreReadingAnchor\(anchor\);\s*\}', new_apply, html_str, count=1)

        # Default language: vi
        html_str = re.sub(r"let lang = readStoredValue\('cloudinsect-lang'\) \|\| 'zh';", "let lang = readStoredValue('cloudinsect-lang') || 'vi';", html_str)
        html_str = re.sub(r"let stored = 'zh';", "let stored = 'vi';", html_str)
        html_str = re.sub(r"localStorage\.getItem\('cloudinsect-lang'\) \|\| 'zh'", "localStorage.getItem('cloudinsect-lang') || 'vi'", html_str)

        # 7. Inject CSS and Surface Script
        html_str = html_str.replace('</head>', VI_CSS + '</head>')
        html_str = html_str.replace('</body>', VI_SURFACE_SCRIPT + '</body>')

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_str)
        print(f"  Updated {html_path}")

def step4_update_root_files():
    print("=== Step 4: Updating root index.html and README.md (v5.2.55, VI and ZH only) ===")
    
    # 1. Update cover image filename if needed
    mahina_cover = os.path.join('assets', 'chapter-banners', 'cover-mahina-profile.jpg')
    ch52_cover = os.path.join('assets', 'chapter-banners', 'chapter-5-wuzhui-2.jpg')
    if os.path.exists(mahina_cover) and not os.path.exists(ch52_cover):
        shutil.copy(mahina_cover, ch52_cover)
        print(f"  Created {ch52_cover}")
        
    root_html_path = 'index.html'
    content = open(root_html_path, encoding='utf-8').read()
    
    # Replace any legacy version strings in attributes or tags
    content = re.sub(r'v5\.(?:1\.39|2\.54)', 'v5.2.55', content)
    content = content.replace('cover-mahina-profile.jpg', 'chapter-5-wuzhui-2.jpg')
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Update version tags
    for el in soup.find_all(class_=['site-version', 'version-badge']):
        el.string = 'v5.2.55'
        
    for el in soup.find_all(attrs={'data-cloudinsect-version': True}):
        el.string = 'v5.2.55'
        
    for meta in soup.find_all('meta', attrs={'name': 'cloudinsect-version'}):
        meta['content'] = 'v5.2.55'
        
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href', '')
        if 'site-footer.css' in href:
            link['href'] = 'assets/site-footer.css?v=5.2.55'
            
    for sc in soup.find_all('script', src=True):
        src = sc.get('src', '')
        if 'site-footer.js' in src:
            sc['src'] = 'assets/site-footer.js?v=5.2.55'
            
    # Clean language-select
    for sel in soup.find_all('select', class_='language-select'):
        sel.clear()
        opt_vi = soup.new_tag('option', value='vi')
        opt_vi.string = 'Tiếng Việt'
        opt_zh = soup.new_tag('option', value='zh')
        opt_zh.string = '简体中文'
        sel.append(opt_vi)
        sel.append(opt_zh)

    # Remove foreign surface scripts
    for sc in soup.find_all('script'):
        for a in list(sc.attrs.keys()):
            if any(x in a for x in ['spanish-surface', 'arabic-surface', 'french-surface', 'ptbr-surface', 'ru-surface']):
                sc.decompose()
                break

    # Remove old injected styles and scripts
    for st in soup.find_all('style', attrs={'data-cloudinsect-vi-style': True}):
        st.decompose()
    for sc in soup.find_all('script', attrs={'data-cloudinsect-vi-surface': True}):
        sc.decompose()
    for lk in soup.find_all('link'):
        href = lk.get('href', '')
        if 'fonts.googleapis.com' in href or 'fonts.gstatic.com' in href:
            lk.decompose()

    # Update data-vi and default static text on root elements
    st = soup.find(id='site-title')
    if st:
        st['data-vi'] = 'Vân Trùng'
        st.string = 'Vân Trùng'
    sub = soup.find(class_='subtitle')
    if sub:
        sub['data-vi'] = 'Chúng ta nhỏ bé tựa kiến cỏ, nhưng lại rực rỡ tựa ngàn sao.'
        sub.string = 'Chúng ta nhỏ bé tựa kiến cỏ, nhưng lại rực rỡ tựa ngàn sao.'
    cat_t = soup.find(class_='catalog-title')
    if cat_t:
        cat_t['data-vi'] = 'Mục lục'
        cat_t.string = 'Mục lục'

    ch_vi_map = {
        '第零章 楔子': 'Chương 0: Mở đầu',
        '第一章 希扬': 'Chương 1: Hi Dương',
        '第二章 云中人 · 一': 'Chương 2: Người Trong Mây · I',
        '第二章 云中人 · 二': 'Chương 2: Người Trong Mây · II',
        '第二章 云中人 · 三': 'Chương 2: Người Trong Mây · III',
        '第三章 光锥之外 · 一': 'Chương 3: Ngoài Nón Ánh Sáng · I',
        '第三章 光锥之外 · 二': 'Chương 3: Ngoài Nón Ánh Sáng · II',
        '第四章 命运之锥 · 一': 'Chương 4: Nón Định Mệnh · I',
        '第四章 命运之锥 · 二': 'Chương 4: Nón Định Mệnh · II',
        '第五章 乌骓 · 一': 'Chương 5: Ô Chuy · I',
        '第五章 乌骓 · 二': 'Chương 5: Ô Chuy · II'
    }
    for cn in soup.find_all(class_='chapter-name'):
        zh_val = cn.get('data-zh', '').strip()
        if zh_val in ch_vi_map:
            cn['data-vi'] = ch_vi_map[zh_val]
            cn.string = ch_vi_map[zh_val]
    for cm in soup.find_all(class_='chapter-meta'):
        cm['data-vi'] = 'Đã phát hành'
        cm.string = 'Đã phát hành'
    for ca in soup.find_all(class_='chapter-action'):
        ca['data-vi'] = 'Bắt đầu đọc'
        ca.string = 'Bắt đầu đọc'

    if soup.title:
        soup.title.string = 'Vân Trùng · Mục lục đọc truyện · v5.2.55'

    # STRIP ALL FOREIGN ATTRIBUTES IN ROOT
    strip_foreign_attributes(soup)

    html_str = str(soup)

    # Update languageMeta in root JS
    new_meta = 'const languageMeta = {"vi": {"htmlLang": "vi", "title": "Vân Trùng · Mục lục đọc truyện · v5.2.55"}, "zh": {"htmlLang": "zh-CN", "title": "云虫 阅读目录 · v5.2.55"}};'
    html_str = re.sub(r'const languageMeta = \{[\s\S]*?\};', new_meta, html_str, count=1)

    # Update root applyLanguage to only handle vi and zh
    root_apply = """function applyLanguage(nextLang) {
        const lang = languageMeta[nextLang] ? nextLang : 'zh';
        document.documentElement.lang = languageMeta[lang].htmlLang;
        document.title = languageMeta[lang].title;
        document.querySelectorAll('[data-zh]').forEach((el) => {
          el.textContent = (lang === 'vi' ? el.dataset.vi : el.dataset.zh) || el.dataset.zh || '';
        });
        const langSelect = document.querySelector('.language-select');
        if (langSelect && langSelect.value !== lang) { langSelect.value = lang; }
        writeStoredValue('cloudinsect-lang', lang);
      }"""
    html_str = re.sub(r'function applyLanguage\(nextLang\) \{[\s\S]*?writeStoredValue\(\'cloudinsect-lang\', lang\);\s*\}', root_apply, html_str, count=1)

    # Default to vi in root
    html_str = re.sub(r"applyLanguage\(readStoredValue\('cloudinsect-lang'\) \|\| 'zh'\);", "applyLanguage(readStoredValue('cloudinsect-lang') || 'vi');", html_str)
    html_str = re.sub(r"let stored = 'zh';", "let stored = 'vi';", html_str)
    html_str = re.sub(r"localStorage\.getItem\('cloudinsect-lang'\) \|\| 'zh'", "localStorage.getItem('cloudinsect-lang') || 'vi'", html_str)

    # Inject root font CSS and surface script
    root_vi_css = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,700&display=swap" rel="stylesheet">
<style data-cloudinsect-vi-style="true">
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('assets/fonts/be-vietnam-pro-400-normal.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url('assets/fonts/be-vietnam-pro-400-italic.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url('assets/fonts/be-vietnam-pro-600-normal.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('assets/fonts/be-vietnam-pro-700-normal.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: italic;
  font-weight: 700;
  font-display: swap;
  src: url('assets/fonts/be-vietnam-pro-700-italic.ttf') format('truetype');
}
@font-face {
  font-family: 'Be Vietnam Pro';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url('assets/fonts/be-vietnam-pro-800-normal.ttf') format('truetype');
}

html[lang="vi"],
html[lang="vi"] body,
html[lang="vi"] * {
  font-family: "Be Vietnam Pro", "Segoe UI", Roboto, -apple-system, BlinkMacSystemFont, Arial, sans-serif !important;
}

html[lang="vi"] #site-title {
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.05;
}

html[lang="vi"] .subtitle {
  font-weight: 500;
  font-style: normal;
  line-height: 1.62;
  letter-spacing: 0.01em;
}

html[lang="vi"] .catalog-title {
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

html[lang="vi"] .chapter-name {
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.3;
}

html[lang="vi"] .chapter-action {
  font-weight: 600;
  letter-spacing: 0.02em;
}

html[lang="vi"] .title-line h1 {
  width: min-content;
}

@media (max-width: 760px) {
  .title-line {
    gap: 12px !important;
  }
  html[lang="vi"] .title-line h1 {
    width: min-content !important;
  }
  .personal-site-entry {
    width: clamp(74px, 18vw, 84px) !important;
    height: clamp(74px, 18vw, 84px) !important;
  }
  .personal-site-label {
    left: -4px !important;
    font-size: clamp(17px, 4.5vw, 20px) !important;
  }
}
</style>
"""
    root_vi_surface = """<script data-cloudinsect-vi-surface="true">
(function () {
  function applyVietnameseSurface() {
    if ((document.documentElement.lang || '').toLowerCase() !== 'vi') return;
    document.querySelectorAll('[aria-label="Language selection"]').forEach((item) => { item.setAttribute('aria-label', 'Chọn ngôn ngữ'); });
    document.querySelectorAll('.language-select').forEach((item) => { item.setAttribute('aria-label', 'Ngôn ngữ'); });
    const catalog = document.querySelector('.catalog');
    if (catalog) catalog.setAttribute('aria-label', 'Mục lục các chương');
    document.querySelectorAll('.cloudinsect-copyright').forEach((item) => { item.textContent = "© WLOP. Toàn bộ nội dung và bản quyền liên quan trên trang web này thuộc về WLOP. Mọi hành vi sao chép, tái bản, cải biên hoặc sử dụng cho mục đích thương mại khi chưa được phép đều bị nghiêm cấm. Bảo lưu mọi quyền."; });
    document.querySelectorAll('.cloudinsect-contact-label').forEach((item) => { item.textContent = "Liên hệ:"; });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', applyVietnameseSurface, { once: true });
  else applyVietnameseSurface();
  window.setTimeout(applyVietnameseSurface, 0);
  const select = document.querySelector('.language-select');
  if (select) select.addEventListener('change', () => setTimeout(applyVietnameseSurface, 0));
}());
</script>
"""
    html_str = html_str.replace('</head>', root_vi_css + '</head>')
    html_str = html_str.replace('</body>', root_vi_surface + '</body>')

    with open(root_html_path, 'w', encoding='utf-8') as f:
        f.write(html_str)
    print(f"  Root {root_html_path} updated.")

    # 2. Update README.md without any Suvan / Mahina
    readme_path = 'README.md'
    readme = open(readme_path, encoding='utf-8').read()
    # Strip any suvan / mahina from readme
    readme = re.sub(r'\(suvan\s*/\s*希扬\)', '(希扬)', readme, flags=re.IGNORECASE)
    readme = re.sub(r'\(mahina\s*/\s*月牙儿\)', '(月牙儿)', readme, flags=re.IGNORECASE)
    readme = re.sub(r'v5\.\d+\.\d+', 'v5.2.55', readme)
    readme = re.sub(r'10 [Cc]hapters?', '11 chapters', readme)
    readme = re.sub(r'10 [Cc]hương', '11 chương', readme)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    print("  README.md updated.")

if __name__ == '__main__':
    all_chapters = []
    step1_update_json(all_chapters)
    step2_generate_markdown()
    step3_update_html_readers()
    step4_update_root_files()
    print("=== ALL STEPS COMPLETED SUCCESSFULLY! ===")
