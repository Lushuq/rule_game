const SceneSystem = {
    currentScene: null,
    visitedScenes: [],

    scenes: {
        entrance: {
            id: 'entrance',
            title: '🏚️ 建筑入口',
            description: `你站在一座老旧建筑的入口前。

锈迹斑斑的铁门在夜风中发出刺耳的吱呀声，仿佛在邀请你进入。

门旁的墙上贴着一张泛黄的告示，上面写着一些模糊不清的规则...

你感觉到有什么东西在注视着你。`,
            choices: [
                { text: '进入建筑', nextScene: 'lobby', addRule: true },
                { text: '阅读墙上的告示', nextScene: 'entrance', addRule: true },
                { text: '犹豫是否要离开', nextScene: 'entrance', addRule: false }
            ]
        },
        lobby: {
            id: 'lobby',
            title: '🏛️ 大厅',
            description: `你进入了宽敞的大厅。

空气中弥漫着陈旧和腐朽的气味。天花板上的吊灯闪烁不定，在墙壁上投下怪异的影子。

前方有一条长长的走廊，左侧是楼梯，右侧是一扇紧闭的门。

角落里有一部老旧的电梯，指示灯显示它停在...负二楼？`,
            choices: [
                { text: '走向走廊', nextScene: 'hallway', addRule: true },
                { text: '登上楼梯', nextScene: 'stairs', addRule: true },
                { text: '打开右侧的门', nextScene: 'study', addRule: false },
                { text: '尝试使用电梯', nextScene: 'elevator', addRule: true }
            ]
        },
        hallway: {
            id: 'hallway',
            title: '🚶 走廊',
            description: `走廊很长，两侧排列着无数扇门。

每扇门上都有一个房间号码，但数字似乎在不断变化...

你听到远处传来轻微的脚步声，越来越近，又突然消失。

墙上的画像中，人物的眼睛好像在跟随你的移动。`,
            choices: [
                { text: '继续向前走', nextScene: 'hallway2', addRule: true },
                { text: '随便打开一扇门', nextScene: 'random_room', addRule: false },
                { text: '回头走向大厅', nextScene: 'lobby', addRule: false },
                { text: '仔细观察墙上的画像', nextScene: 'hallway', addRule: true }
            ]
        },
        hallway2: {
            id: 'hallway2',
            title: '🚶 走廊深处',
            description: `走廊似乎没有尽头。

你感觉已经走了很久，但周围的景色完全没有变化。

脚步声又响起了，这次就在你身后...

但当你猛地回头，身后空无一物。`,
            choices: [
                { text: '不顾一切地向前跑', nextScene: 'dining_hall', addRule: true },
                { text: '慢慢转过身去', nextScene: 'anomaly_scene', addRule: false },
                { text: '闭上眼睛数到十', nextScene: 'hallway2', addRule: true },
                { text: '寻找其他出口', nextScene: 'lobby', addRule: false }
            ]
        },
        stairs: {
            id: 'stairs',
            title: '🪜 楼梯间',
            description: `楼梯盘旋向上，消失在黑暗中。

你数着台阶...一阶，两阶，三阶...但很快就数不清了。

楼梯间里异常安静，只能听到你自己的心跳声和脚步声的回响。

向上看，一片漆黑；向下看，同样是无尽的黑暗。`,
            choices: [
                { text: '继续向上走', nextScene: 'attic', addRule: true },
                { text: '向下走', nextScene: 'basement', addRule: true },
                { text: '回到大厅', nextScene: 'lobby', addRule: false },
                { text: '在楼梯上坐下来休息', nextScene: 'stairs', addRule: true }
            ]
        },
        elevator: {
            id: 'elevator',
            title: '🛗 电梯',
            description: `电梯门缓缓打开，里面空无一人。

控制面板上有很多按钮，但只有几层楼的按钮是亮着的。

你注意到负二楼的按钮一直在闪烁。

当你踏入电梯的瞬间，温度似乎骤降了几度。`,
            choices: [
                { text: '按下去二楼的按钮', nextScene: 'basement', addRule: true },
                { text: '按下去一楼的按钮', nextScene: 'study', addRule: false },
                { text: '按下去三楼的按钮', nextScene: 'bedroom', addRule: true },
                { text: '退出电梯', nextScene: 'lobby', addRule: false }
            ]
        },
        study: {
            id: 'study',
            title: '📚 书房',
            description: `这是一间堆满书籍的书房。

书架上的书排列得整整齐齐，但书脊上的书名你一个都不认识。

书桌中央放着一本打开的日记，字迹还很新...

角落里有一个古老的保险箱，转盘上刻着奇怪的符号。`,
            choices: [
                { text: '阅读日记', nextScene: 'study', addRule: true },
                { text: '从书架上拿一本书', nextScene: 'study', addRule: false },
                { text: '尝试打开保险箱', nextScene: 'anomaly_scene', addRule: false },
                { text: '离开书房', nextScene: 'lobby', addRule: false }
            ]
        },
        dining_hall: {
            id: 'dining_hall',
            title: '🍽️ 餐厅',
            description: `一张巨大的餐桌摆满了丰盛的食物。

但所有的食物都已经腐烂，散发着令人作呕的气味。

餐桌旁坐着几个...人？他们一动不动，似乎在等待什么。

墙上的钟表显示的时间是...12:61？`,
            choices: [
                { text: '坐下和他们一起用餐', nextScene: 'anomaly_scene', addRule: false },
                { text: '询问他们这里发生了什么', nextScene: 'dining_hall', addRule: true },
                { text: '仔细观察墙上的钟表', nextScene: 'dining_hall', addRule: true },
                { text: '赶紧离开餐厅', nextScene: 'hallway', addRule: false }
            ]
        },
        bedroom: {
            id: 'bedroom',
            title: '🛏️ 卧室',
            description: `这是一间儿童卧室。

床上放着一个破旧的布娃娃，它的眼睛似乎在看着你。

墙上用蜡笔画了很多画，内容让人感到不安...

衣柜的门微微开着一条缝，里面很黑。`,
            choices: [
                { text: '查看床上的布娃娃', nextScene: 'bedroom', addRule: true },
                { text: '仔细看墙上的蜡笔画', nextScene: 'bedroom', addRule: false },
                { text: '打开衣柜', nextScene: 'anomaly_scene', addRule: false },
                { text: '离开卧室', nextScene: 'hallway', addRule: false }
            ]
        },
        attic: {
            id: 'attic',
            title: '🏚️ 阁楼',
            description: `阁楼上堆满了旧家具和箱子。

灰尘很厚，看起来很多年没人来过了。

角落里有一面落地镜，但镜子里照不出你的身影...

透过阁楼的窗户，你看到外面的世界...不太对劲。`,
            choices: [
                { text: '看向那面镜子', nextScene: 'anomaly_scene', addRule: true },
                { text: '打开几个箱子看看', nextScene: 'attic', addRule: false },
                { text: '透过窗户向外看', nextScene: 'attic', addRule: true },
                { text: '下楼回到楼梯间', nextScene: 'stairs', addRule: false }
            ]
        },
        basement: {
            id: 'basement',
            title: '🔦 地下室',
            description: `地下室很潮湿，水滴声不断。

空气中弥漫着一股奇怪的气味...生锈的金属？或者...

墙壁上有很多划痕，像是某种生物留下的痕迹。

走廊尽头有一扇铁门，门后传来低沉的咆哮声。`,
            choices: [
                { text: '走向那扇铁门', nextScene: 'anomaly_scene', addRule: true },
                { text: '仔细观察墙上的划痕', nextScene: 'basement', addRule: false },
                { text: '在地下室里探索', nextScene: 'basement', addRule: true },
                { text: '回到电梯', nextScene: 'elevator', addRule: false }
            ]
        },
        random_room: {
            id: 'random_room',
            title: '🚪 奇怪的房间',
            description: `你打开了一扇门，里面是...

这是什么地方？你认不出来，但又觉得很熟悉。

房间里的布置似乎在不断变化，你眨了眨眼，家具就换了位置。

你突然意识到，这个房间...正在盯着你。`,
            choices: [
                { text: '在房间里四处看看', nextScene: 'random_room', addRule: true },
                { text: '立即关上门离开', nextScene: 'hallway', addRule: false },
                { text: '尝试和房间里的...存在交流', nextScene: 'anomaly_scene', addRule: true },
                { text: '闭上眼睛，想象自己在大厅', nextScene: 'lobby', addRule: false }
            ]
        },
        anomaly_scene: {
            id: 'anomaly_scene',
            title: '⚠️ 异常发生',
            description: `...

（触发异常事件）`,
            choices: [
                { text: '继续...', nextScene: 'lobby', addRule: false }
            ],
            isAnomaly: true
        }
    },

    getScene(sceneId) {
        return this.scenes[sceneId];
    },

    setCurrentScene(sceneId) {
        if (this.scenes[sceneId]) {
            this.currentScene = this.scenes[sceneId];
            if (!this.visitedScenes.includes(sceneId)) {
                this.visitedScenes.push(sceneId);
            }
            return this.currentScene;
        }
        return null;
    },

    getCurrentScene() {
        return this.currentScene;
    },

    getNextScene(choiceIndex) {
        if (this.currentScene && this.currentScene.choices[choiceIndex]) {
            return this.currentScene.choices[choiceIndex].nextScene;
        }
        return null;
    },

    shouldAddRule(choiceIndex) {
        if (this.currentScene && this.currentScene.choices[choiceIndex]) {
            return this.currentScene.choices[choiceIndex].addRule;
        }
        return false;
    },

    reset() {
        this.currentScene = null;
        this.visitedScenes = [];
    }
};
