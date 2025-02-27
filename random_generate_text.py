# -*- coding: utf-8 -*-
import random
import argparse
import multiprocessing
from tqdm import tqdm

dictionary = """!#%&'()*+, -./0123456789:<=>@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_`abcdefghijklmnopqrstuvwxyz~¥々あいうぇえおかがきぎくぐけげこごさざしじすずせそぞただちっつづてでとどなにぬねのはばひびふぶべほぼぽまみむめもゃやゆょよらりるれろわをん゙゚ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロワンヴヶ・一丁七万三上下不与世丘丙両並中串丸丹主乃久之乙九乳亀予亊事二互五井亜交京亭人仁今介仏付仙代仮仲任企伊伎伏会伝伯伸似佃住佐体余作依便保信俣修倉倍借倶偕健側備働優元先光免児兜入全八公六共兵具兼内円再写冨冶冷出函刀分切刈初別利到刷券前剛剤割創劇力加助労勇動務勝勢勧勿匂包化北匝匠区医十千半卒協南博占卯印卸厚原参又友双反取受口古可台右号司各合吉同名吐向君吹吾呂呉告周味呼命和咲品員唐商問善喜喰営嘉器四団国國園土在地坂坊坪垂型垣城域基埼堀堂堅堤堰報場堺塗塚塩塾境墓増墨壁壗士壬壱売夏夕外多夜夢大天太夫央奇奈奉奥女好妙妻姥姫威婁婦媛子字孝季学孫宅宇守安宏宕宗官宙定宜宝実客室宮害家容宿寄密富寒寝寮寺寿専射尊小尻尼尽尾局居屋属山岐岡岩岬岱岳岸峠峯峰島崎嶋嶺川州巣工左差巳巻巽市布希帝師帯常帽幅幌幕幡幣干平年幸庁広庄店府座庫庭庵康廣延建廿弁式弐弓引弘弥張当形彦彩影彼待律後御徳心忍志忠念忽急恒恩恵悠悪情惣愛慈慣慶懸成我戸房所扇手才打技折押拓拾持指振挽掛採推揚援損携摂摩摺撫播支改放政教敦整敷文斉斎斐斗料斧新方於施旅旗旙日旦早旭昇昌明易星春昭是時晃景晴智暁暮曇曙曲曳更書曽曾替最會月有服望朝木未末本札朱杉杏材村杜束条来東杵松板析林枚果枝枡柄柏染柚柳柴査柿栃栄栖栗校株根桂桃桐桑桔桜桶梅梗條梨械梶棚棟森椋植椎検椥椿楠楡楢業極楽榎榛榮榴構様槻樋模権横樫樹樺樽橋橘機橿櫛欠次歌止正此武歯歳段殻殿母比毛氏民気水氷永氾汐江池沓沖沢河油治沼泉泊法波泥泰洋洗洞津洲活流浄浅浜浦浪浮海消淀淡深淵添清済渋渕渚渡温測港湊湖湘湛湯湾満源溝滋滑滝漁潟潮澄澤濁濃濤濱瀬灘火災烏無然焼照熊熱燃燕父爺片版牛牟牡牧物特犬狛狩独狭狼猛猪猫猿玄玉王珂珠現球理琉琴瑞瑠瑳璃環瓜瓦甘生産用田由甲男町画界畑留畜畠番畿病療発登白百的皆皮皿益盛盟盤目直相県眞真眼着督矢知石砂研砥砧破砺硝碑碧磐磨磯礼社祇祉祐祖神祥祭福秀秋科秦秩税稜種稲穀穂積穴究空窪竈立竜童竪端竹竿笛笠笥第笹等筋筑筒筬箕算管箪箱築篠篭米籾粕粟精糀糧糸紀紅紋納紙紡紫細紺組経結絡給絹継続綜維綱網綵綾綿総緑線練縄縫繊織纏置美群義羽翁習翔老者耕耶聖聞職肉肝肥育胡能脇脚腰膝膳臨自臼興舎舗舘舞舟般船良色芋芙芝芦花芳芸芹芽苅苑苗若苫英茂茄茅茨茶草荏荒荘荷荻莱菅菊菓菖菜華菱萩萬萱落葉葛葦葬葵葺蒲蒼蓉蓬蓮蔵蕨薙薩薬薮藍藤蘭虎虻蛇蛎蝶行術街衛衡衣表袋装裏製裾西要覇見親観角觜計訓記訪設証誉語誠読課調諏諫諸警議護谷豆豊豪貝財貨販貫責貴貿賀資赤走起越足趾路蹟車軍軒軽輝輪輸辰農辺辻込近迦迫追送逆透逗通速造連進遊運道達遠遣邑那邦郎郡部郭郵郷都配酒釈里重野量金釜針釧鈎鈑鈴鉄鉢鉱鉾銀銅銘銚鋳鋺鋼錦録鍋鍛鍬鎌鎗鏡鑑長門開間関閤阜阪防阿陀限院陣陵陶陸険陽隅隆隈階際障隠隼雀雄雅集雑離難雨雪雲電霊霞霧露青静非面韮音頃順須領頭額類風飛食飯飼飽飾養館首香馬駄駅駐駒駿験骨高髪鬼魚鮎鮒鯖鳥鳩鳳鳴鴛鴨鴫鴬鴻鵜鵠鶏鶯鶴鷲鷹鷺鹿麗麹麻黒鼻齊龍﨑"""

def get_random_textline(dummy):
    len_textline = random.randint(10, 50)
    text = ''
    for _ in range(len_textline):
        text += random.choice(dictionary)
    return text


def main(args):
    # output_list = []
    pool = multiprocessing.Pool(args.num_workers)
    output_list = list(tqdm(pool.imap(get_random_textline, list(range(args.num_textlines))),
                            total=args.num_textlines, desc="Generating"))
    pool.terminate()
    with open(args.output_path, 'w') as f:
        for textline in output_list:
            f.write("%s\n" % textline)
    print('Dumped to', args.output_path, '. Done!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get random Japanese and Latin textline')
    parser.add_argument('--output_path', default='./data/newsgroup/newsgroup.txt',
                        type=str, required=False, help='path to the generated .txt text file')
    parser.add_argument('--num_textlines', default=10000, type=int,
                        required=False, help='number of textlines to generate')
    parser.add_argument('--num_workers', default=32, type=int,
                        required=False, help='number of core use for multiprocessing')
    args = parser.parse_args()
    main(args)
