<template>
  <Layout>
    <Header style="fontSize: 3em; fontWeight: bolder; color: white">
      智能家居管理系统
      <Dropdown class="Dropdown mHeader">
        <Avatar icon="ios-person" size="large" />
        <template #list>
          <DropdownMenu>
            <DropdownItem>
              <Button @click="showRegModal = true" type="text">注册</Button>
            </DropdownItem>
            <DropdownItem v-if="logState">
              <Button type="text">登出</Button>
            </DropdownItem>
            <DropdownItem v-else>
              <Button @click="showLogInModal = true" type="text">登录</Button>
            </DropdownItem>
          </DropdownMenu>
        </template>
        <Modal v-model="showRegModal" title="用户注册" footer-hide>
          <!-- 密码 用户名 手机号 -->
          <Form :model="userInfo" style="margin: 20px 30px 0 30px">
            <FormItem prop="userName">
              <Input
                type="text"
                size="large"
                v-model="userInfo.userName"
                placeholder="用户名至少为6位"
              >
                <template #prepend>
                  <Icon type="ios-person-outline"></Icon>
                </template>
              </Input>
            </FormItem>
            <FormItem prop="phoneNumber">
              <Input
                type="tel"
                size="large"
                v-model="userInfo.phoneNumber"
                placeholder="11位手机号"
              >
                <template #prepend>
                  <Icon type="ios-phone-portrait" />
                </template>
              </Input>
            </FormItem>
            <FormItem prop="password1">
              <Input
                type="password"
                password
                size="large"
                v-model="userInfo.password1"
                placeholder="密码至少为6位"
              >
                <template #prepend>
                  <Icon type="ios-lock-outline"></Icon>
                </template>
              </Input>
            </FormItem>
            <FormItem prop="password2">
              <Input
                type="password"
                password
                size="large"
                v-model="userInfo.password2"
                placeholder="两次请输入相同的密码"
              >
                <template #prepend>
                  <Icon type="ios-lock-outline"></Icon>
                </template>
              </Input>
            </FormItem>
            <FormItem>
              <Button
                style="float: right"
                size="large"
                type="primary"
                @click="handleRegister()"
                >注册</Button
              >
            </FormItem>
          </Form>
        </Modal>
        <Modal v-model="showLogInModal" title="用户登录" footer-hide>
          <Form :model="logInInfo" style="margin: 20px 30px 0 30px">
            <FormItem prop="userName">
              <Input
                type="text"
                size="large"
                v-model="logInInfo.userName"
                placeholder="用户名"
              >
                <template #prepend>
                  <Icon type="ios-person-outline"></Icon>
                </template>
              </Input>
            </FormItem>
            <FormItem prop="userName">
              <Input
                type="password"
                password
                size="large"
                v-model="logInInfo.password"
                placeholder="密码"
              >
                <template #prepend>
                  <Icon type="ios-lock-outline"></Icon>
                </template>
              </Input>
            </FormItem>
            <FormItem>
              <Button
                style="float: right"
                size="large"
                type="primary"
                @click="handleLogin()"
                >登录</Button
              >
            </FormItem>
          </Form>
        </Modal>
      </Dropdown>
    </Header>
    <!-- 场景创建表单 -->
    <Content>
      <div style="margin: 20px; float: right">
        <Form inline :model="sceneInfo">
          <FormItem>
            <Input size="large" placeholder="场景名称需唯一"
              v-model='sceneInfo.sceneName'><template #prepend>场景名称</template></Input>
          </FormItem>
          <FormItem>
            <Upload action="//jsonplaceholder.typicode.com/posts/">
              <Button size='large' icon="ios-cloud-upload-outline">Upload files</Button>
            </Upload>
          </FormItem>
          <FormItem>
            <Button size="large" type="primary" @click='handleCreateScene()'>创建场景</Button>
          </FormItem>
        </Form>
      </div>
      <div style='width: 90%; margin-left: auto; margin-right: auto;'>
        <SceneTable style='margin-left: auto; margin-right: auto;'/>
      </div>
    </Content>
    <Footer>{{ copyright }}</Footer>
  </Layout>
</template>

<script>
/* eslint-disable */
import SceneTable from './SceneTable.vue'
export default {
  name: "Test",
  components: {
    SceneTable: SceneTable
  },
  data() {
    return {
      showRegModal: false,
      showLogInModal: false,
      logState: false,
      copyright: "copyright @ WuXinbei 2022",
      userInfo: {
        userName: "",
        phoneNumber: "",
        password1: "",
        password2: "",
      },
      logInInfo: {
        userName: "",
        password: "",
      },
      sceneInfo: {
        sceneName: "",
      }
    };
  },
  methods: {
    handleRegister() {
      let userName = this.userInfo.userName;
      let phoneNumber = this.userInfo.phoneNumber;
      let password1 = this.userInfo.password1;
      let password2 = this.userInfo.password2;
      // check null
      if (userName === undefined || userName.length == 0) {
        this.$Message["error"]({
          background: true,
          content: "用户名不可以为空",
        });
        return;
      }
      if (phoneNumber === undefined || phoneNumber.length == 0) {
        this.$Message["error"]({
          background: true,
          content: "手机号不可以为空",
        });
        return;
      }
      if (
        password1 === undefined ||
        password1.length == 0 ||
        password2 === undefined ||
        password2.length == 0
      ) {
        this.$Message["error"]({ background: true, content: "密码不可以为空" });
        return;
      }
      // check length
      if (userName.length < 6) {
        this.$Message["error"]({
          background: true,
          content: "用户名至少为6位",
        });
        return;
      }
      if (phoneNumber.length != 11) {
        this.$Message["error"]({ background: true, content: "手机号不合法" });
        return;
      }
      if (password1 !== password2) {
        this.$Message["error"]({
          background: true,
          content: "两次密码输入不一致",
        });
        return;
      }
      if (password1.length < 6) {
        this.$Message["error"]({
          background: true,
          content: "密码长度至少为6位",
        });
        return;
      }
      // todo 后端传数据、校验手机号和用户名的唯一性、注册用户并反馈

      this.$Message["success"]({ background: true, content: "注册成功" });
    },
    handleLogin() {
      let userName = this.logInInfo.userName;
      let password = this.logInInfo.password;
      console.log(this.logInInfo);
      if (userName === undefined || userName.length == 0) {
        this.$Message["error"]({
          background: true,
          content: "用户名不可以为空",
        });
        return;
      }
      if (password === undefined || password.length == 0) {
        this.$Message["error"]({ background: true, content: "密码不可以为空" });
        return;
      }
      // todo 校验用户名和密码匹配 返回登录结果
    },
    handleCreateScene() {
      // todo OSS
      // todo implement upload
      // todo implement server store
    }
  },
};
</script>

<style>
.Dropdown {
  font-size: 16px;
  margin-left: 20px;
}

.mHeader {
  float: right;
}
</style>
