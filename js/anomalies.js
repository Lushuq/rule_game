const AnomalySystem = {
    anomalyCount: 0,
    maxAnomalies: 5,

    anomalyEvents: [
        {
            title: '👁️ 被注视',
            description: `你感觉到无数双眼睛在注视着你。

它们从墙壁里、从地板下、从天花板上，从每一个阴影中看着你。

你想移开视线，但你的眼睛不听使唤...`,
            effect: 'glitch'
        },
        {
            title: '⏰ 时间异常',
            description: `墙上的钟表开始疯狂地旋转。

时间在倒流，又在加速，反反复复。

你不知道现在是什么时候，也不知道自己在这里待了多久...`,
            effect: 'flicker'
        },
        {
            title: '👻 低语声',
            description: `你听到了低语声。

很多很多的低语声，在你的耳边，在你的脑海里。

它们在说什么？你听不清，但你知道它们在谈论你...`,
            effect: 'sound'
        },
        {
            title: '🖼️ 变化的环境',
            description: `周围的一切都在变化。

墙壁在融化，地板在蠕动，天花板在呼吸。

这座建筑...它是活的。`,
            effect: 'distortion'
        },
        {
            title: '🚪 无尽的门',
            description: `你看到无数扇门在你面前出现又消失。

每扇门的后面是什么？你不敢去想。

但你知道，你必须选择一扇...`,
            effect: 'shake'
        },
        {
            title: '🪞 镜中异象',
            description: `你在镜子里看到了自己。

但那不是你。

它在微笑，笑得很开心...`,
            effect: 'glitch'
        },
        {
            title: '👣 脚步声',
            description: `脚步声。

从四面八方传来的脚步声。

越来越近，越来越近...`,
            effect: 'sound'
        },
        {
            title: '📝 规则崩坏',
            description: `你收集的规则开始在你眼前扭曲。

字迹在流淌，在改变，在互相吞噬。

哪些规则是真的？哪些规则是假的？你已经分不清了...`,
            effect: 'distortion'
        },
        {
            title: '🌑 黑暗降临',
            description: `所有的光线都消失了。

你陷入了完全的、绝对的黑暗中。

但你能感觉到，有什么东西在黑暗中，离你很近很近...`,
            effect: 'darkness'
        },
        {
            title: '🫂 触碰',
            description: `有什么东西碰到了你。

冰冷的、湿滑的、让人作呕的触碰。

它在你的皮肤上爬行，想要进入你的身体...`,
            effect: 'shake'
        }
    ],

    gameOverReasons: [
        '你违反了太多规则，这座建筑已经对你失去了耐心...',
        '异常的累积已经超过了临界值，现实开始崩塌...',
        '你看到了不该看的东西，它们注意到了你...',
        '规则的矛盾撕裂了现实，你被卷入了虚无...',
        '这座建筑饿了，而你是它选中的晚餐...'
    ],

    triggerAnomaly(violatedRule) {
        this.anomalyCount++;
        
        const event = this.anomalyEvents[Math.floor(Math.random() * this.anomalyEvents.length)];
        
        return {
            ...event,
            violatedRule: violatedRule,
            count: this.anomalyCount,
            isGameOver: this.anomalyCount >= this.maxAnomalies
        };
    },

    getGameOverReason() {
        return this.gameOverReasons[Math.floor(Math.random() * this.gameOverReasons.length)];
    },

    reset() {
        this.anomalyCount = 0;
    },

    canContinue() {
        return this.anomalyCount < this.maxAnomalies;
    }
};
