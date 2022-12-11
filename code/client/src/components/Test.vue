<template>
  <Layout>
    <Header style="fontSize: 3em; fontWeight: bolder; color: white">
      智能家居管理系统
      <Dropdown class="Dropdown mHeader">
        <Avatar v-show="logState" icon="ios-person" size="large" style="background-color: #87d468"/>
        <Avatar v-show="enableCreateScene" icon="ios-person" size="large" />
        <template #list>
          <DropdownMenu>
            <DropdownItem>
              <Button @click="showRegModal = true" type="text">注册</Button>
            </DropdownItem>
            <DropdownItem v-if="logState">
              <Button @click="handleLogOut" type="text">登出</Button>
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
    <Content style="background:#fff">
      <div style="margin: 20px; float: right">
        <Form inline :model="sceneInfo" >
          <FormItem>
            <Input size="large" placeholder="场景名称需唯一"
              v-model='sceneInfo.sceneName'><template #prepend>场景名称</template></Input>
          </FormItem>
          <FormItem>
            <input type="file" @change="getImageFile" id="img">
          </FormItem>
          <FormItem>
            <Button size="large" type="primary" @click='upload' :disabled="enableCreateScene">创建场景</Button>
          </FormItem>
        </Form>
      </div>
      <div style='width: 90%; margin-left:auto; margin-right:auto' >
        <SceneTable :sceneData="sceneData" style="margin-left:auto; margin-right:auto" />
      </div>
    </Content>
    <Footer style='width:100%; height:25px; padding:3px; position: fixed; bottom: 0px'>{{ copyright }}</Footer>
  </Layout>
</template>

<script>
/* eslint-disable */
import SceneTable from './SceneTable.vue'
import axios from 'axios'
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
        uid: "",
        userName: "",
        password: "",
      },
      sceneInfo: {
        sceneName: "",
        file: null,
      },
      sceneData: [],
    };
  },
  computed: {
    enableCreateScene() {
      return this.logState == true ? false : true
    },
    logIconColor() {
      return this.logState == true ? "blue" : "gray"
    }
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
      let phoneReg = /^[1][3,4,5,7,8][0-9]{9}$/ // 检验手机号是否合法
      if (phoneNumber.length != 11 || !phoneReg.test(phoneNumber)) {
        this.$Message["error"]({ background: true, content: "手机号不合法！" });
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
      axios.post('http://127.0.0.1:8000/user/signup', this.userInfo)
        .then((res)=>{
          res = res.data.state 
          if (res === 1) {
            this.$Message["warning"]({ background: true, content: "用户名已存在，请使用其他用户名" });
          } else if (res === 2) {
            this.$Message["warning"]({ background: true, content: "手机号已存在，请使用其他手机号" });
          } else {
            this.$Message["success"]({ background: true, content: "注册成功" });
            this.showRegModal = false
          }
        })
      
    },
    handleLogin() {
      let userName = this.logInInfo.userName;
      let password = this.logInInfo.password;
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
      axios.post('http://127.0.0.1:8000/user/login', this.logInInfo).then(res=>{
        let logRes = res.data.state
        if (logRes == 2) {
          this.$Message["error"]({ background: true, content: "密码不正确" });
        } else if (logRes == 1) {
          this.$Message["error"]({ background: true, content: "用户不存在，请检查用户名" });
        } else {
          this.$Message["success"]({ background: true, content: "登录成功" });
          this.logState = true
          this.logInInfo.uid = res.data.id
          console.log(res.data.sceneData)
          this.sceneData = res.data.sceneData
          this.showLogInModal = false
        }
      })
    },
    handleLogOut() {
      this.logState = false
      this.logInInfo.uid = ""
      this.logInInfo.userName = ""
      this.logInInfo.password = ""
      this.$Message["info"]({ background: true, content: "成功登出"})
    },
    getImageFile:function(e) {
      this.sceneInfo.file = e.target.files[0]
    },
    upload() {
      let data = new FormData()
      if (this.logInInfo.userName === undefined || this.logInInfo.userName === "") {
        this.$Message['warning']({background: true, content:"请先登录！"})
        return 
      }
      data.append('userName', this.logInInfo.userName)
      if (this.sceneInfo.sceneName === undefined || this.sceneInfo.sceneName === "") {
        this.$Message['warning']({background: true, content:"请先完善场景名称！"})
        return 
      }
      data.append('sceneName', this.sceneInfo.sceneName)
      data.append('uid', this.logInInfo.uid)
      if (this.sceneInfo.file === null) {
        this.$Message['warning']({background: true, content:"请先上传文件！"})
        return 
      }
      data.append('oriImage', this.sceneInfo.file)
      this.$Message['info']({background: true, content:"正在上传文件~"})
      axios.post('http://127.0.0.1:8000/scene/create', data)
      .then(res => {
        let state = res.data
        if (state == 1) {
          this.$Message['warning']({ background: true, content: "场景名已经存在，请使用其他名称"})
        } else if (state == 2) {
          this.$Message['error']({ background: true, content: "图片上传失败，请检查网络情况"})
        } else {
          this.$Message['success']({ background: true, content: "场景创建成功"})
          this.sceneInfo.sceneName = ""
          this.sceneInfo.file = null
          this.file = null
          this.sceneData = res.data.sceneData
        }
      })
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
