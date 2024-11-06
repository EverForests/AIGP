<template>
  <div>
    <header>
      <h1>AIGP</h1>
      <p>欢迎来到AIGP智能图像处理网站！</p>
    </header>

    <div class="container">
      <h2>我们的特色功能</h2>
      <div class="features">
        <Feature title="文生图" description="文生图是一款强大的图像编辑工具，它可以帮助您轻松编辑图像，添加各种滤镜、调整色调、裁剪图像等。"></Feature>
        <Feature title="图生图" description="图生图是一款方便易用的批量处理工具，它可以让您一次性处理多张图像，节省您的时间和精力。"></Feature>
        <Feature title="高清化" description="高清化工具可以将图像转换为高清格式，提高图像的清晰度和质量，满足您对图像质量的不同需求。"></Feature>
      </div>
    </div>
  </div>
</template>

<script>
import Feature from '../components/Feature.vue';
import axios from 'axios';
import router from '@/router';

export default {
  name: "HomeView",
  components: {
    Feature
  },
  setup() {
    axios.get('/book/v1/articles', {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(
        response => {
          console.log(response.data);
        }
      )
      .catch(
        error => {
          console.error('Error: ', error);
        }
      )

    const ddd = () => {
      router.push({ name: 'userprofile', params: { userId: 2 } })
    }

    const siderStyle = {
      textAlign: 'center',
      lineHeight: '120px',
      color: '#fff',
      backgroundColor: '#3ba0e9',
    };

    const footerStyle = {
      textAlign: 'center',
      color: '#fff',
      backgroundColor: '#7dbcea',
    };

    const contentStyle = {
      textAlign: 'center',
      minHeight: 120,
      lineHeight: '120px',
      color: '#fff',
      // backgroundColor: '#108ee9',
      padding: '0 50px',
    };

    return {
      ddd,
      siderStyle,
      footerStyle,
      contentStyle,
    }
  }
}
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

header {
  background-color: #333;
  color: #fff;
  padding: 20px;
  text-align: center;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-top: 0;
}

.features {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}


/* 测试 */
.site-layout-content {
  min-height: 280px;
  padding: 24px;
  background: #fff;
}

#components-layout-demo-top .logo {
  float: left;
  width: 120px;
  height: 31px;
  margin: 16px 24px 16px 0;
  background: rgba(255, 255, 255, 0.3);
}

.ant-row-rtl #components-layout-demo-top .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme='dark'] .site-layout-content {
  background: #141414;
}

.layout {
  height: 100vh;
}
</style>
