<template>
    <span>
        <div 
            v-for="m in mana_costs"
            :key="m"
            :class="m"
        ></div>
    </span>
</template>

<script>

export default {
    props: ['cost'],
    data: () => ({
        mana_costs: []
    }),
    created() {
        console.log(this.cost)
        const regex = /([0-9WBRGU]+)/g;
        let matches = this.cost.match(regex)
        matches.forEach(element => (function(scope){
            scope.mana_costs = scope.mana_costs.concat(`mana_cost mana_icon_${element}`)
        })(this));
        console.log(this.mana_costs)
    },
}
</script>

<style>

.mana_cost {
    height: 16px;
    width: 16px;
    background: url('/images/mana_cost_sprites.gif') no-repeat;
    display: inline-block;
    padding: 1px;
}

.mana_icon_0 {
    background-position: 0px 0px;
}

.mana_icon_1 {
    background-position: 0px -16px;
}

.mana_icon_2 {
    background-position: 0px -32px;
}

.mana_icon_2B {
    background-position: 0px -48px;
}

.mana_icon_2G {
    background-position: 0px -64px;
}

.mana_icon_2R {
    background-position: 0px -80px;
}

.mana_icon_2U {
    background-position: 0px -96px;
}

.mana_icon_2W {
    background-position: 0px -112px;
}

.mana_icon_3 {
    background-position: 0px -128px;
}

.mana_icon_4 {
    background-position: 0px -144px;
}

.mana_icon_5 {
    background-position: 0px -160px;
}

.mana_icon_6 {
    background-position: 0px -176px;
}

.mana_icon_7 {
    background-position: 0px -192px;
}

.mana_icon_8 {
    background-position: 0px -208px;
}

.mana_icon_9 {
    background-position: 0px -224px;
}

.mana_icon_10 {
    background-position: 0px -240px;
}

.mana_icon_11 {
    background-position: 0px -256px;
}

.mana_icon_12 {
    background-position: 0px -272px;
}

.mana_icon_13 {
    background-position: 0px -288px;
}

.mana_icon_14 {
    background-position: 0px -304px;
}

.mana_icon_15 {
    background-position: 0px -320px;
}

.mana_icon_16 {
    background-position: 0px -336px;
}

.mana_icon_B {
    background-position: 0px -352px;
}

.mana_icon_BG {
    background-position: 0px -368px;
}

.mana_icon_BR {
    background-position: 0px -384px;
}

.mana_icon_G {
    background-position: 0px -400px;
}

.mana_icon_GU {
    background-position: 0px -416px;
}

.mana_icon_GW {
    background-position: 0px -432px;
}

.mana_icon_R {
    background-position: 0px -448px;
}

.mana_icon_RG {
    background-position: 0px -464px;
}

.mana_icon_RW {
    background-position: 0px -480px;
}

.mana_icon_S {
    background-position: 0px -496px;
}

.mana_icon_snow {
    background-position: 0px -512px;
}

.mana_icon_tap {
    background-position: 0px -528px;
}

.mana_icon_U {
    background-position: 0px -544px;
}

.mana_icon_UB {
    background-position: 0px -560px;
}

.mana_icon_untap {
    background-position: 0px -576px;
}

.mana_icon_UR {
    background-position: 0px -592px;
}

.mana_icon_W {
    background-position: 0px -608px;
}

.mana_icon_WB {
    background-position: 0px -624px;
}

.mana_icon_WU {
    background-position: 0px -640px;
}

.mana_icon_X {
    background-position: 0px -656px;
}


</style>
