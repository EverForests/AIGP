<template>
    <div class="feature">
        <h2>{{ title }}</h2>
        <p>{{ description }}</p>
    </div>
</template>

<script>
export default {
    props: {
        title: String,
        description: String
    }
}
</script>

<style scoped>
.feature {
    width: calc(33.33% - 20px);
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
}

.feature h2 {
    margin-top: 0;
}

.feature p {
    color: #666;
}
</style>
