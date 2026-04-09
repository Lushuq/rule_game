const RuleSystem = {
    rules: [],
    ruleIdCounter: 1,

    ruleTemplates: [
        {
            category: 'movement',
            templates: [
                { text: '不要在[时间]进入[房间]', type: 'forbidden' },
                { text: '在[时间]必须待在[房间]', type: 'mandatory' },
                { text: '进入[房间]前必须[动作]', type: 'condition' },
                { text: '离开[房间]后不能[动作]', type: 'forbidden' }
            ]
        },
        {
            category: 'action',
            templates: [
                { text: '看到[事物]时必须[动作]', type: 'mandatory' },
                { text: '听到[声音]时不要[动作]', type: 'forbidden' },
                { text: '当[事件]发生时，立即[动作]', type: 'condition' },
                { text: '无论发生什么，都不要[动作]', type: 'absolute' }
            ]
        },
        {
            category: 'social',
            templates: [
                { text: '如果遇到[角色]，不要[动作]', type: 'forbidden' },
                { text: '当[角色]说话时，必须[动作]', type: 'mandatory' },
                { text: '不要相信[角色]说的任何话', type: 'absolute' },
                { text: '只有[角色]可以信任', type: 'absolute' }
            ]
        },
        {
            category: 'time',
            templates: [
                { text: '每过[数字]分钟，规则可能会变化', type: 'info' },
                { text: '在[时间]之后，之前的规则全部作废', type: 'overriding' },
                { text: '当钟声敲响[数字]次时，[事件]将会发生', type: 'condition' }
            ]
        },
        {
            category: 'item',
            templates: [
                { text: '永远不要放下[物品]', type: 'absolute' },
                { text: '看到[物品]时必须立刻捡起', type: 'mandatory' },
                { text: '持有[物品]时，你可以[动作]', type: 'condition' },
                { text: '如果[物品]消失，立刻[动作]', type: 'condition' }
            ]
        }
    ],

    placeholders: {
        time: ['午夜', '凌晨三点', '黄昏', '正午', '任意时刻'],
        room: ['走廊', '电梯', '楼梯间', '地下室', '阁楼', '图书馆', '餐厅', '卧室'],
        action: ['回头', '说话', '呼吸', '移动', '眨眼', '开门', '关灯'],
        thing: ['影子', '镜子', '窗户', '门', '画作', '雕像', '照片'],
        sound: ['脚步声', '低语声', '敲门声', '笑声', '哭声', '钟声'],
        event: ['灯光闪烁', '温度骤降', '时间停止', '门自行打开'],
        character: ['管理员', '清洁工', '小女孩', '老人', '戴面具的人'],
        number: ['三', '五', '七', '九', '十三'],
        item: ['钥匙', '蜡烛', '手电筒', '日记本', '照片', '护身符']
    },

    generateRule() {
        const category = this.ruleTemplates[Math.floor(Math.random() * this.ruleTemplates.length)];
        const template = category.templates[Math.floor(Math.random() * category.templates.length)];
        
        let text = template.text;
        const matches = text.match(/\[(\w+)\]/g);
        
        if (matches) {
            matches.forEach(match => {
                const key = match.slice(1, -1);
                if (this.placeholders[key]) {
                    const replacement = this.placeholders[key][Math.floor(Math.random() * this.placeholders[key].length)];
                    text = text.replace(match, replacement);
                }
            });
        }

        const rule = {
            id: this.ruleIdCounter++,
            text: text,
            type: template.type,
            category: category.category,
            createdAt: Date.now(),
            status: 'active',
            contradicts: [],
            overriddenBy: null
        };

        this.rules.push(rule);
        this.checkForContradictions(rule);
        return rule;
    },

    checkForContradictions(newRule) {
        this.rules.forEach(rule => {
            if (rule.id !== newRule.id && rule.status === 'active') {
                if (this.rulesContradict(rule, newRule)) {
                    rule.contradicts.push(newRule.id);
                    newRule.contradicts.push(rule.id);
                }
            }
        });
    },

    rulesContradict(rule1, rule2) {
        if (rule1.type === 'absolute' && rule2.type === 'absolute') {
            return Math.random() > 0.5;
        }
        if ((rule1.type === 'mandatory' && rule2.type === 'forbidden') ||
            (rule1.type === 'forbidden' && rule2.type === 'mandatory')) {
            return Math.random() > 0.3;
        }
        if (rule1.type === 'overriding') {
            return true;
        }
        return Math.random() > 0.8;
    },

    overrideOldRules() {
        const activeRules = this.rules.filter(r => r.status === 'active');
        if (activeRules.length > 5 && Math.random() > 0.5) {
            const ruleToOverride = activeRules[Math.floor(Math.random() * activeRules.length)];
            ruleToOverride.status = 'overridden';
            
            const newRule = this.generateRule();
            newRule.overrides = ruleToOverride.id;
            ruleToOverride.overriddenBy = newRule.id;
            
            return newRule;
        }
        return null;
    },

    getActiveRules() {
        return this.rules.filter(r => r.status === 'active');
    },

    getRuleById(id) {
        return this.rules.find(r => r.id === id);
    },

    checkRuleViolation(action, context) {
        const activeRules = this.getActiveRules();
        for (const rule of activeRules) {
            if (this.doesViolateRule(rule, action, context)) {
                return rule;
            }
        }
        return null;
    },

    doesViolateRule(rule, action, context) {
        const violationChance = 0.3 + (rule.contradicts.length * 0.1);
        return Math.random() < violationChance;
    },

    reset() {
        this.rules = [];
        this.ruleIdCounter = 1;
    }
};
