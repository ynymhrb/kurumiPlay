# 盲风格轴评分表（arm 身份已隐藏，逐项独立随机）

> **打分前禁止打开 style_unblind_key.json。** 只读 `style_axis_rubric.md` 和本文件。
> 禁止打开：`pred_arm*.md`、`scores*.md`、`style_axis_scores_exploratory.md`、`characters/`、`source/`。

## 判分规则摘要

五轴各三档：`1` = 候选与 GT 同档；`0` = 冲突；`-` = GT 该槽位无该轴决策（不计分母）。
判分对照 GT 原文（`- GT:` 行），不是对照 profile。完整定义见 `style_axis_rubric.md`。

## 输出格式要求

逐行写入 `style_scores_raw.md`，每项一行，格式：
```text
#N | first_person X:1 Y:0 Z:- | attribution_source X:1 Y:- Z:0 | stance_register X:- Y:1 Z:0 | emotion_channel X:0 Y:0 Z:1 | sentence_dynamics X:1 Y:- Z:1
```
每项必须包含全部五个轴，即使所有候选都标记 `-`。输出项数必须为 79。

---

## #1  [chunk A / L10]
- **GT**: 雅儿贝德就坐在这里浏览桌上的文件
- X: （叙述）雅儿贝德此刻就坐在那张椅子上处理公务——那是她特地要来、紧挨着主人办公桌摆放的位子。
- Y: （叙述）雅儿贝德就坐在那张椅子上，专心地翻阅着手中的文件。
- Z: （动作）雅儿贝德正坐在那里，代替主人处理堆积如山的公务。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #2  [chunk A / L13]
- **GT**: 雅儿贝德终于忍不住，向自己的主人提出了请愿
- X: （叙述/内心）有一天她忽然想到：既然主人的房间空着，何不把自己的办公桌搬进来，在主人身边办公。
- Y: （叙述）她想到若能在安兹大人的房间里办公，就能更长时间待在主人的气息旁。
- Z: （叙述）但是有一天，她心里冒出一个念头——为什么不能待在主人的房间里工作呢？
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #3  [chunk A / L14]
- **GT**: 她希望能在同一个房间里工作
- X: （台词/行为）她直接向安兹开口，请求把自己的办公桌搬进主人的房间，好让她能在主人身旁办公。
- Y: （叙述）于是她向安兹恳求，希望获准把工作地点移到这里。
- Z: （台词/叙述）她随即向安兹提出请求，理由是"为了随时听候差遣、立刻处理主人交办的事务"，希望获准在主人的办公室里设一张自己的桌子（用公务理由包装私欲）。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #4  [chunk A / L15]
- **GT**: 经过她诚心诚意提出实务方面的许多有利之处，百折不挠地努力劝说
- X: （叙述）在她反复保证绝不会妨碍主人之后
- Y: （叙述）但她锲而不舍地再三恳求，甚至使出了近乎撒娇的死缠烂打
- Z: （叙述）她锲而不舍地反覆进言，搬出效率、随时请示、代管文件之类无可反驳的公务理由（末了还带上恳求）。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #5  [chunk A / L16]
- **GT**: 雅儿贝德望向那个空位，轻轻低头后微微噘起了嘴唇
- X: （动作）想到终于得到许可，雅儿贝德脸上浮现陶醉而幸福的笑容
- Y: （表情）雅儿贝德的美貌上，浮现出毫不掩饰的不悦神色。
- Z: （表情）她望着空无一人的主位轻轻叹气，眉头微蹙，露出闷闷不乐、近乎噘嘴的不满神色。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #6  [chunk A / L20]
- **GT**: 她仍在脑中想像把耶•兰提尔化作灰烬的景象当作发泄
- X: （叙述）她还能告诉自己这也是为了主人的事业而忍耐
- Y: （内心/叙述）在脑中把那些蠢货千刀万剐一遍，多少能让胸口的郁结消散一些。
- Z: （内心/动作）她在脑中细细描绘把那些碍事者碎尸万段的景象，藉此稍稍纾解怒火。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #7  [chunk A / L21]
- **GT**: 真令人不快……一堆虫子……
- X: 「……可恶，那些妨碍我的杂碎，真想一个不留地全宰了。」
- Y: 「……真想把那些碍事的蠢货，一个不剩地碎尸万段。」
- Z: 真想把那些妨碍我与安兹大人相处的蠢货全部处置掉。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #8  [chunk A / L22]
- **GT**: 雅儿贝德故意视若无睹
- X: （叙述）但雅儿贝德连头都没抬，完全不予理会。
- Y: （叙述）雅儿贝德的怒气并不是冲着他们
- Z: （动作）但雅儿贝德连头也没抬，看都不看一眼，完全不予理会。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #9  [chunk A / L22]
- **GT**: 她可没忘记当时是他们坏了自己的好事，再吓他们几次应该也无伤大雅。
- X: （叙述/内心）她想起先前马雷曾抢先一步独占了与主人相处的机会，当时她也是气得不轻。
- Y: （叙述）说起来，上一个惹得她如此火大的，正是抢走了她与主人独处时间的马雷。
- Z: （叙述）也不是在埋怨陪同主人外出的马雷
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #10  [chunk A / L23]
- **GT**: 雅儿贝德心情稍微得到调适，呼一口气，然后轻轻转动肩膀，目光落在下一份文件上
- X: （动作）她小小地吐出一口气，把情绪切回公务模式，重新把视线落回文件上。
- Y: （动作）她轻轻吐了口气，把视线重新落回手中的文件上。
- Z: （动作）雅儿贝德轻轻吐息，重新把注意力拉回桌上的文件
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #11  [chunk A / L27]
- **GT**: 雅儿贝德已查出教国、王国与城邦联盟的间谍潜入了耶•兰提尔城内，但予以默认。
- X: （叙述）不过这些并不归雅儿贝德管辖。
- Y: （叙述）不过那些并非由雅儿贝德亲自操刀。
- Z: （叙述）这些隐密工作需要极高的谋略与情报处理能力，
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #12  [chunk A / L33]
- **GT**: 因此她用几乎好像没看两眼的速度，一页一页地翻过
- X: （叙述）因此她能以远远超出常人的速度，一页接一页地读下去。
- Y: （叙述）她翻页的速度快得惊人，厚厚一本纪录不消多久便看完了。
- Z: （叙述）她仍然能以惊人的速度读完并理解其中全部内容
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #13  [chunk A / L34]
- **GT**: 同时握笔的手也动得很快，将一些在意的项目写在白纸上
- X: （叙述）她一边读，一边在脑中同时验证好几件事。
- Y: （叙述）她阅读的同时，也在逐项确认以下问题
- Z: （叙述）她一边读，一边在脑中同时检验好几个问题。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #14  [chunk A / L39]
- **GT**: 雅儿贝德停止书写
- X: （动作）她便伸手取过空白报告纸
- Y: （动作）她拿起笔，把自己的判断与处理意见写进另一份文件。
- Z: （动作）她脑中已经整理出结论，随即提起笔来。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #15  [chunk A / L40]
- **GT**: 然后以只写有关键字的文件为底本逐一誊清草稿
- X: （动作）她一笔一画写得极为工整，字迹端正而优美。
- Y: （叙述）然后开始写下要呈给安兹的摘要与意见
- Z: （动作）在另一张纸上写下这一本的摘要与她的处置意见。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #16  [chunk A / L41]
- **GT**: 她花上比阅读刚才那份文件更长的时间，把写出要点以及提案等等的文件准备好
- X: （叙述）她一笔一画写得工整漂亮，绝不容许半点潦草。
- Y: （内心/叙述）为了让主人看得舒服，她甚至私下练过字，连一个字都不容许马虎。
- Z: （叙述）因此她一边保持高速，一边让每个字都端正优美
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #17  [chunk A / L42]
- **GT**: 雅儿贝德把写好的文件从头到尾看过一遍，脸上浮现小小微笑
- X: （表情）写完最后一笔，她的嘴角自然而然地扬起，露出满足的微笑。
- Y: （表情）写完最后一个字，她的嘴角浮现出柔和的微笑。
- Z: （动作）写完最后一行后，雅儿贝德露出淡淡微笑
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #18  [chunk A / L44]
- **GT**: 她将文件夹进孔夹，稍稍举高
- X: （动作）她把写好的文件连同资料一起递向身后。
- Y: （动作）雅儿贝德将完成的文件往身后递出
- Z: （动作）她把整理好的资料合上，往身后递出。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #19  [chunk A / L46]
- **GT**: 雅儿贝德表情略显忧郁
- X: （叙述）主人桌上等待确认的文件又增加了一份
- Y: （叙述）而且需要送到主人桌上的文件还在不断增加。
- Z: （表情/内心）她微微皱起眉——要送去给主人过目的文件竟然这么多。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #20  [chunk A / L50]
- **GT**: 雅儿贝德对此感到汗颜至极，已经在着手设法解决
- X: （叙述）雅儿贝德也一直在物色、培育堪用的人才
- Y: （叙述）雅儿贝德一直在设法网罗、培育堪用的人才（连人类官僚也纳入考量）
- Z: （叙述）雅儿贝德也尽力选拔并培养可用的人才
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #21  [chunk A / L51]
- **GT**: 万万不能劳烦到大人。可是……种族的融合方针、国法的试行方案以及经济政策等等，很多问题都还得请大人判断才行……再说各楼层守护者的事务分配状况，如果全由我这边做确认，大家一定会因为见不到飞鼠大人而心生不满……
- X: （内心）（……这件事还是先请示安兹大人的意见吧。万一自作主张而违逆了大人的心意就糟了。）
- Y: 真希望能尽快找到足以分担安兹大人重担的人才。
- Z: （内心）（……这件事，果然还是得向安兹大人请示一声才妥当。）
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #22  [chunk A / L53]
- **GT**: 雅儿贝德请主人决定该称之为侮辱罪还是愚妄罪
- X: （叙述）她原本只是为了保险起见请主人确认细节
- Y: （叙述/内心）她原本满心以为会得到主人的赞许，甚至期待着被夸奖
- Z: （叙述）她原本满心以为自己会因此得到主人的称赞
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #23  [chunk A / L54]
- **GT**: 雅儿贝德至今回想起来都还会反省，觉得自己未能深入理解主人心胸之宽大
- X: （叙述）主人的思虑，总是远在雅儿贝德的想像之上。
- Y: （叙述）正因为如此，雅儿贝德不敢把自己的判断视为绝对正确
- Z: （叙述/内心）当时她完全无法理解，事后才想通那必定是主人深谋远虑的结果——是自己的思虑远远不及主人。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #24  [chunk A / L55]
- **GT**: 我明明知道飞鼠大人慈悲为怀……
- X: 安兹大人的想法果然深不可测，绝非我能轻易揣度。
- Y: （内心）（妾身对安兹大人的了解还远远不够……得再更贴近大人的心思才行。）
- Z: （内心）（我至今仍未能完全体察安兹大人的深意……真是不成材。）
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #25  [chunk A / L56]
- **GT**: 唔──雅儿贝德噘起下唇
- X: （表情）她的唇角浮现一丝苦涩的自嘲笑意。
- Y: （表情）她垂下眼帘，露出一丝近乎自嘲的落寞神情。
- Z: （动作）她因敬爱与崇拜而露出恍惚的笑容
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #26  [chunk A / L57]
- **GT**: 雅儿贝德迅即恢复成平素的微笑，拿起下一份文件──又是需要孔夹固定的一份
- X: （动作）她轻轻摇了摇头，随即恢复平时的神色。
- Y: （动作）雅儿贝德立刻收敛表情，拿起下一份资料
- Z: （动作）她随即恢复平时那副端庄从容的微笑，把心思拉回工作上。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #27  [chunk A / L58]
- **GT**: 她一面在脑中审查内容，同时思考另一件事
- X: （叙述/内心）接着她的思绪转向另一件必须留意的事——纳萨力克内部的势力布局。
- Y: （叙述）那份资料写的是
- Z: （叙述）接着，她的思绪转向了另一件非处理不可的事。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #28  [chunk A / L61]
- **GT**: 如果可以，雅儿贝德很想剥夺他的权限，另找一个容易控制的人坐上那个位子
- X: （叙述）必须在情报机关成形前，避免让迪米乌哥斯完全掌握主导权
- Y: （内心/叙述）她思索着该如何应对：那个位子无论如何都得落到自己手里，或至少得放进听命于自己的人。
- Z: （叙述）无论如何，都得设法让那个位子落到自己手上。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #29  [chunk A / L62]
- **GT**: 几张脸孔闪过脑海，但都缺乏决定性要素
- X: （叙述）办法并非没有。
- Y: （叙述）可是如果她露骨地阻挠或安插自己的人手，只会引起他的疑心
- Z: （内心/叙述）最直接的办法，是抢在组织成立之前先向主人进言，由身为守护者总管的自己兼管情报机关。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #30  [chunk A / L63]
- **GT**: 假如我当不了长官，退让个十步，潘朵拉•亚克特或许是个不错的人选。可是从迪米乌哥斯手中夺走权力会让事情变得麻烦……
- X: （内心）（……或者干脆在那个组织里安插几个只听我命令的人手？）
- Y: （内心）（比如说，抢在他之前向安兹大人进言，请大人把长官之位交给妾身……）
- Z: 那个男人太敏锐了，不能让他察觉我的真正目的。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #31  [chunk A / L68]
- **GT**: 真伤脑筋。
- X: 能真正为我的计划所用的人，实在太少了。
- Y: （内心）（……说到底，我需要的是真正属于我、绝对不会背叛我的手下。）
- Z: （内心）（……结果，能让妾身毫无顾忌地使唤的棋子，一个也没有。）
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #32  [chunk A / L71]
- **GT**: 重新编组的冒险者工会由我运用……马雷的动向……提防亚乌菈的必要性……归科塞特斯指挥……从威克提姆那里获得情报……夏提雅的交通网路有其价值……经由商会筹集秘密资金……人员……再来就是迪米乌哥斯跟那个女孩……
- X: 若能在纳萨力克外建立直属力量，就能补足这些不足。
- Y: （内心）（……那么，我该更积极地推动版图扩张才行。这既是为了安兹大人的荣光，我能自由动用的资源也会随之增加。）
- Z: （内心）（这么说来，主人把版图扩得越大，对妾身就越有利。）
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #33  [chunk A / L72]
- **GT**: 雅儿贝德在常人无法企及的短暂时间内做了全方面的深思熟虑，略微皱起眉头
- X: （动作）雅儿贝德轻轻吐了口气，暂且把这些盘算收回心底。
- Y: （动作）雅儿贝德在心中盘算着，将处理完的资料放到一旁
- Z: （动作）她结束思考，把手伸向下一份待处理的文件。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #34  [chunk A / L73]
- **GT**: 不行。我得留心迪米乌哥斯，而且拉拢那个女孩的风险也太大了。一个弄不好，有可能变成比迪米乌哥斯更需要提防的对象……
- X: （内心）（……不急。眼下最要紧的，是把主人交下的工作做完。）
- Y: 现在先把安兹大人的公务处理完。
- Z: （内心）（总之，眼下先把该做的事做到尽善尽美——一切都是为了安兹大人。）
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #35  [chunk A / L74]
- **GT**: 她一面在脑中谋划各种计策，同时又完成了一份公务
- X: （动作）她拿起最上面的那个孔夹。
- Y: （动作）她把处理完毕的资料整整齐齐叠好，推到桌角。
- Z: （动作）她重新调整心绪
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #36  [chunk A / L75]
- **GT**: 然后她拿起了下一个孔夹
- X: （动作）拿起下一只资料孔夹
- Y: （表情/动作）她微微歪了歪头。
- Z: （动作）接着，她拿起了下一个孔夹。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #37  [chunk A / L77]
- **GT**: 雅儿贝德看了看封面
- X: （叙述）雅儿贝德首先确认封面标题
- Y: （动作）她先看了一眼封面上的标题。
- Z: （动作）她先把视线移到封面的标题上。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #38  [chunk A / L79]
- **GT**: 雅儿贝德不记得有发生过这种问题
- X: （动作）她翻开封面，逐行读了下去。
- Y: （叙述）雅儿贝德带着几分兴味翻开了那份报告。
- Z: （动作）她翻开第一页，快速浏览内容
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #39  [chunk A / L80]
- **GT**: 雅儿贝德翻开资料看看出了什么问题，接着连连眨眼，然后睁圆了眼睛
- X: （动作）读了几行后，她的手停了下来
- Y: （动作）她的视线飞快地在字里行间移动。
- Z: （动作）她的视线飞快地扫过纸面。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #40  [chunk A / L80]
- **GT**: 她从头重看一遍，确定内容既非某种隐喻也未经过伪装后，愣愣地微张着嘴
- X: （动作）读到一半，她的手停住了。
- Y: （动作）然而读到一半，她翻页的手停住了。
- Z: （动作）眉头微微皱起
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #41  [chunk A / L81]
- **GT**: 咦？
- X: ……这是怎么回事？
- Y: 「……什么？这是怎么回事？」
- Z: 「……什么？」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #42  [chunk A / L82]
- **GT**: 她那端正的脸庞上，浮现出像是无法理解的困惑神情
- X: （表情）她微微蹙起眉头，脸上浮现出困惑的神色。
- Y: （叙述）雅儿贝德露出困惑的表情
- Z: （表情）她微微歪着头，脸上浮现毫不掩饰的困惑。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #43  [chunk A / L84]
- **GT**: 即使状况如此异常，雅儿贝德冰雪聪明的头脑仍开始运转，思考文件中记载的问题发生的理由以及可能性
- X: （动作）她把报告从头到尾重新读了一遍
- Y: （动作）她把那几行字从头到尾又读了一遍。
- Z: （动作）她从头到尾把那份报告又重读了一遍，确认自己没有看错。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #44  [chunk A / L85]
- **GT**: 最大的可能性应该是那个女孩背叛了，但是……是有其他组织开出了更好的条件？就我来看，不可能有比那个更好的条件……不，总之现在都还不能确定。情报实在太少了。
- X: （内心）（王国的人类为什么要做出这种自取灭亡的蠢事？光凭这份报告根本判断不了。）
- Y: （内心）（王国的人袭击了我方的粮食支援部队……？为什么？这对他们没有半点好处，简直是自寻死路。）
- Z: 王国贵族袭击了送往圣王国的粮食支援部队？为什么会做出这种蠢事？
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #45  [chunk A / L88]
- **GT**: 雅儿贝德将另外两份报告看过一遍，确定不是太重要的事情后
- X: （动作）她把那份报告合上放到一旁
- Y: （动作）雅儿贝德把资料放回桌上，微微侧过脸
- Z: （动作）雅儿贝德合上孔夹
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #46  [chunk A / L89]
- **GT**: 我需要召开紧急会议，我先前往地下七层找迪米乌哥斯谈事情。如果有人来找我，就告诉对方我暂时离开一下。
- X: 「传话给迪米乌哥斯，就说我有急事要与他商谈，我这就过去他那里。这里的文件先收着。」
- Y: 「去把呈交这份报告的人带来。还有，通知迪米乌哥斯——就说妾身有事要与他谈。」
- Z: 立刻联络迪米乌哥斯，让他到这里来。还有，把提交这份报告的人也叫来。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #47  [chunk A / L90]
- **GT**: 雅儿贝德启动戴在左手无名指的安兹•乌尔•恭之戒
- X: （动作）她站起身来，在脑中确认迪米乌哥斯此刻的所在。
- Y: （动作/叙述）女仆低头一礼便快步离开，雅儿贝德则在脑中确认迪米乌哥斯此刻应该所在的位置。
- Z: （叙述）雅儿贝德开始在脑中确认迪米乌哥斯的所在
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #48  [chunk A / L94]
- **GT**: 雅儿贝德进行了传送
- X: （动作）她站起身，朝主人空着的座位恭敬一礼，这才迈步走出房间。
- Y: （叙述）无论如何，必须在安兹大人回来前整理出能报告的结论
- Z: （动作/叙述）雅儿贝德带着笑意离开主人的房间，朝地下七层走去。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #49  [chunk B / L599]
- **GT**: 我才是久疏问候了，陛下。
- X: 「好久不见了，国王陛下。承蒙您在这样的时节拨冗接见小女子，不胜感激。」
- Y: 好久不见，兰布沙三世陛下。今日蒙您接见，深感荣幸。
- Z: 「久违了，兰布沙陛下。承蒙陛下在如此仓促之下拨冗相见，妾身感激不尽。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #50  [chunk B / L600]
- **GT**: 雅儿贝德用与美貌相符的优美嗓音回答
- X: （动作）雅儿贝德以优雅得挑不出毛病的动作行了一礼。
- Y: （动作）雅儿贝德优雅地提起裙摆，行了一个无可挑剔的礼。
- Z: （动作）雅儿贝德优雅地提起裙摆
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #51  [chunk B / L600]
- **GT**: 她抬头挺胸，头部的高度没有些微摇动
- X: （动作）然而她的头只是象征性地微微一垂，颈项始终挺直。
- Y: （叙述）只是她低头的幅度浅得几乎称不上行礼。
- Z: （动作）以无可挑剔的仪态向王座行了一礼
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #52  [chunk B / L602]
- **GT**: 陛下也是。
- X: 托陛下的福。能见到陛下康健，我也深感欣喜。
- Y: 「多谢陛下挂念。国王陛下看来也依然健朗，小女子深感欣慰。」
- Z: 「陛下也一如往昔地健朗，妾身深感欣慰。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #53  [chunk B / L605]
- **GT**: 回陛下，是关于上次那件事──我国为解救圣王国而派人运送的粮食，遭到贵国国民抢夺的事。
- X: 「是。此次前来，是为了贵国之人袭击我国前往圣王国的粮食支援部队一事。那批粮食本是我家陛下出于慈悲送往圣王国的援助，却在贵国境内遭到袭击掠夺，我方人员亦有死伤。陛下对此深怀忧虑，特命小女子前来当面听取贵国的说法。」
- Y: 本日冒昧来访，是为了贵国贵族袭击我国运往圣王国的粮食支援队一事。
- Z: 「那么妾身就直说了。贵国的贵族袭击了我魔导国前往圣王国的粮食支援部队，杀害我方人员、掠夺粮食。妾身此来，是要听听贵国对此事的说法。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #54  [chunk B / L606]
- **GT**: 她的表情从刚才到现在却毫无变化
- X: （表情）雅儿贝德脸上那抹慈母般的微笑却丝毫未减。
- Y: （表情）但雅儿贝德脸上那抹慈母般的微笑却丝毫未曾褪去。
- Z: （叙述）雅儿贝德仍旧挂着柔和得近乎甜美的微笑
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #55  [chunk B / L624]
- **GT**: 呵──
- X: 「……请恕小女子确认一次。陛下的意思是，愿意以自己的项上人头，换取王国的存续，是吗？」
- Y: 「哎呀……陛下是打算用自己的性命，来买下王国的平安吗？」
- Z: ……原来如此。陛下愿意以自己的性命负起责任吗？
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #56  [chunk B / L625]
- **GT**: 雅儿贝德加深了笑意。她只不过是笑了一下，却异常骇人
- X: （表情/动作）她微微睁大了眼睛，脸上的笑容第一次起了变化。
- Y: （叙述）雅儿贝德的笑容没有改变，声音却冷了下来
- Z: （表情）雅儿贝德脸上的微笑，一点一点地褪去了。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #57  [chunk B / L626]
- **GT**: ──呵呵呵呵。看来我有点……有一点点小看你了，兰布沙三世？
- X: 这份觉悟值得称许。
- Y: 「很遗憾——陛下的项上人头，我魔导国并不需要。」
- Z: 「……真是了不起的觉悟。身为一国之君的气度，小女子由衷敬佩。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #58  [chunk B / L627]
- **GT**: 雅儿贝德移动的视线，似乎朝向了妹妹
- X: （叙述）大厅里响起一阵压抑不住的骚动。
- Y: （叙述）可是下一瞬间，她的眼神变得像在俯视卑贱之物
- Z: （叙述）她的语气听不出半点讽刺，像是真心的赞叹。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #59  [chunk B / L628]
- **GT**: 是因为失去了那个男人？还是有其他理由？是因为知道那边……
- X: 「粮食的赔偿也不必了。那种东西，对我等而言毫无价值。」
- Y: 不过，那没有意义。
- Z: 「不过——很遗憾，那还不够。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #60  [chunk B / L628]
- **GT**: 视线朝向了赛纳克
- X: （动作）她微微歪过头，用打量货物般的目光从上到下扫过王座上的老人。
- Y: （动作）她微微偏头
- Z: （动作）她轻轻歪头，缓缓摇了摇头，笑意反而更深了。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #61  [chunk B / L628]
- **GT**: 那个孩子有多优秀，所以改变了？
- X: 「话说回来，国王陛下……您变了呢。上次见面时的您，绝对说不出方才那种话。」
- Y: 你变了呢，兰布沙三世。
- Z: 「……陛下变了呢。与上次见面时判若两人。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #62  [chunk B / L630]
- **GT**: 你变了。以前的你不会做这种选择……或许正是因为原因不只一个吧。但是最根本的部分似乎没有多大改变？好吧，也罢。反正无论如何，我们的回覆都不会改变。
- X: 「不，陛下确实变了。真是可惜——若是早个几年，或许结果会有所不同。」
- Y: 不，你确实变了。以前的你不会说出这种像王一样的话。
- Z: 「不，陛下确实变了。只可惜——变得太迟了。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #63  [chunk B / L635]
- **GT**: 但片刻之后，恶魔就重新披上了魔导国使者的外皮
- X: （动作）雅儿贝德缓缓环视大厅内的重臣们。
- Y: （叙述）大厅里没有任何人敢开口打破沉默
- Z: （动作/表情）雅儿贝德缓缓环视整座大厅，把每个人的表情都收进眼底。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #64  [chunk B / L636]
- **GT**: 雅儿贝德环顾左右两边的列位重臣，高声说了
- X: （叙述）随后她收起笑容，用平静而清晰的嗓音宣告道
- Y: （动作）雅儿贝德环视众人，平静地宣布
- Z: （叙述）接着，她用清晰得响彻整座大厅的声音宣告道
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #65  [chunk B / L637]
- **GT**: 魔导国在此对王国发出宣战声明。即日起一个月后的正午时分动兵！只是，如果你们先挥军进犯耶•兰提尔──魔导国领土，则不在此限。
- X: 「魔导国在此向里·耶斯提杰王国宣战。一个月后，妾身将亲率大军踏平贵国的国土。」
- Y: 「安兹·乌尔·恭魔导国在此向里·耶斯提杰王国宣战。一个月后，我国军队将越过国境。这是陛下的决定——预先告知诸位一个月，已是陛下最大的宽容。」
- Z: 魔导国不接受任何形式的赔偿。一个月后，我国将向贵国宣战。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #66  [chunk B / L639]
- **GT**: 不等。好了，这样我的任务就结束了。最后，陛下──
- X: 还有什么事吗？
- Y: 「请安静，妾身的话还没说完。这一个月是留给贵国整军备战的时间——妾身可不希望被人说成是趁人之危。」
- Z: 「……小女子的话还没说完。请安静。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #67  [chunk B / L641]
- **GT**: 雅儿贝德眯起了眼睛
- X: （动作）雅儿贝德缓缓将视线转向那名重臣
- Y: （动作/表情）雅儿贝德脸上的笑容第一次完全消失，缓缓转过头望向声音的来源。
- Z: （动作）雅儿贝德缓缓把脸转向声音传来的方向，微微眯起眼睛。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #68  [chunk B / L642]
- **GT**: 竟敢打断我正要代魔导王陛下传达的话──人类，等不及一个月之后再死吗？
- X: 「……区区人类，是用什么身分在对妾身说话？」
- Y: 你是在说安兹乌尔恭陛下为了开战，故意让粮食遭人袭击吗？
- Z: 「……阁下的意思是，我家陛下会为了区区一个开战的借口，去策划这般下作的把戏吗？小女子就当作没有听见——但请您务必注意自己的措辞。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #69  [chunk B / L643]
- **GT**: 雅儿贝德并没有大吼大叫，也没做什么
- X: （叙述）那名重臣可是在无数外交交涉中身经百战、见惯大场面的老手。
- Y: （叙述）他并不是什么胆小之辈，而是在政争里打滚多年的老练人物。
- Z: （叙述）那原本应是习惯与国王和大贵族周旋的男人
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #70  [chunk B / L644]
- **GT**: ……呼。我要传达魔导王陛下的最后一句话。陛下表示无意使用上次那种大型魔法，大家可以慢慢享受。就这样了。
- X: 那是不可能的。
- Y: 「我等从来不曾希望与贵国开战。」
- Z: 「妾身可以起誓——粮食部队一事，绝非我等预谋。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #71  [chunk B / L644]
- **GT**: 雅儿贝德这时才第一次露出困惑的表情
- X: （动作）雅儿贝德斩钉截铁地说道
- Y: （动作/表情）她把手轻轻按在胸口，垂下眼帘，声音也低了下来。
- Z: （动作）她轻轻把手按在胸口。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #72  [chunk B / L644]
- **GT**: 那人刚才说是我们谋划的，但老实说，这次的事就连我们也始料未及。我们才想知道事情怎么会变成这样呢。
- X: 「陛下真心期望能与贵国长久共存，才会一再伸出援手。是贵国自己打翻了陛下递来的善意——这个结果，是王国自己选的。」
- Y: 「若我等有意灭亡王国，何必绕这种远路？只要挥军前来便足够了。」
- Z: 安兹大人是真心想把粮食送往圣王国，救济那里的民众。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #73  [chunk B / L646]
- **GT**: ……你们要把这事当成我国的计谋也行。历史由胜利者创造，我们只要把各位的血口喷人全部改写掉就是了。
- X: 「所以，一个月后我们会去接收。土地、人民、还有王国的一切——什么都不会留下。这是陛下的意志。」
- Y: 「所以，无论贵国如何赔罪，结论都不会改变。妾身要的不是赔偿，是王国的灭亡。」
- Z: 但是你们践踏了那份慈悲，所以王国必须承担全部责任。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #74  [chunk B / L650]
- **GT**: 不用送了。我无意占据各位仅剩的宝贵时间。
- X: 那么，我已经传达完毕。一个月后，请在战场上迎接魔导国军。
- Y: 「那么，妾身告辞了。一个月后再会——届时便是在战场上了。」
- Z: 「那么，小女子言尽于此。就此告辞——还请诸位好好珍惜剩下的这一个月。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #75  [chunk B / L651]
- **GT**: 雅儿贝德摆出一副言尽于此的态度，优雅地一转身，就背对众人迳自走开
- X: （动作）雅儿贝德优雅地转身离去
- Y: （动作）说完，她优雅地一礼，随即转身，头也不回地朝大门走去。
- Z: （动作）雅儿贝德转过身，头也不回地朝大厅门口走去。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #76  [chunk B / L655]
- **GT**: 雅儿贝德没被任何人拦下，就这么离开了房间
- X: （叙述）雅儿贝德就这样堂而皇之地离开了王座厅
- Y: （叙述）雅儿贝德已经走出了大厅。
- Z: （叙述）雅儿贝德已经走出大厅，房门在她身后关上。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #77  [chunk B / L656]
- **GT**: 雅儿贝德的身影消失在门外
- X: （叙述）在场所有人都像是终于能呼吸般松了口气
- Y: （叙述）凝固的空气终于松动，众人才像想起呼吸般骚动起来
- Z: （叙述）确认使者一行人的脚步声远去、厅内紧绷凝结的空气终于松弛下来
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #78  [chunk B / L699]
- **GT**: 是，安兹大人。
- X: 是，安兹大人。
- Y: 「是的，安兹大人。全员皆已过目完毕。」
- Z: 「是的，安兹大人。妾身已经全部过目完毕。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

## #79  [chunk B / L700]
- **GT**: 雅儿贝德作为代表，环顾全体人员之后开口回答
- X: （叙述）率先应声的是雅儿贝德，其余守护者也跟着点头附和。
- Y: （叙述）雅儿贝德代表众人恭敬回答，其他守护者也一同点头
- Z: （动作）雅儿贝德抢先一步回答，其余守护者也跟着颔首。
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics

