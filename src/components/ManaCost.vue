<template>
    <div class="mana_cost"></div>
</template>

<script>

export default {
    props: ['cost']
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

</style>
