<template>
  <div>
    <Table size='large' style="width:100%" stripe border :columns="columns" :data='displayData'></Table>
    <Drawer width="700" v-model='showEquipmentInfo' placement='left' title='设备信息'>
      <Table size='large' stripe border :columns="equipmentColumns" :data="equipmentData"></Table>
    </Drawer>
    <Modal v-model="showEditEquipment" style="width:400px" footer-hide>
      <Form :model="certainEquipment" style='margin:40px'>
        <FormItem>
          设备编号:
          <Input style="width: auto" v-model='certainEquipment.id' disabled></Input>
        </FormItem>
        <FormItem>
          设备名称:
          <Input style="width: auto" v-model='certainEquipment.name' disabled></Input>
        </FormItem>
        <FormItem>
          设备类型:
          <Input style="width: auto" v-model='certainEquipment.type' disabled></Input>
        </FormItem>
        <FormItem>
          设备状态:
          <Input style="width: auto" v-model='certainEquipment.state'></Input>
        </FormItem>
        <FormItem>
          <Button size="large" type="primary" @click='handleEditEquipment'>确认上报</Button>
        </FormItem>
      </Form>
    </Modal>
    <Modal v-model="showAddEquipment" style="width:400px" footer-hide>
      <Form :model="equipToAddData" style="margin: 40px">
        <FormItem>
          场景编号:
          <Input style="width:auto" v-model="equipToAddData.sceneNo" disabled></Input>
        </FormItem>
        <FormItem>
          设备名称:
          <Input style="width:auto" v-model="equipToAddData.name" placeholder="设备名称需唯一" required></Input>
        </FormItem>
        <FormItem>
          设备类型:
          <Select v-model="equipToAddData.type" style="width:200px" required>
            <Option v-for="item in equipmentType" :value="item.key" :key="item.key">{{ item.name }}</Option>
          </Select>
        </FormItem>
        <FormItem>
          设备状态:
          <Input number style="width:250px" v-model="equipToAddData.state" placeholder=" 灯(亮度)温度(℃)湿度(%)门锁开关(1/0) " required></Input>
        </FormItem>
        <FormItem>
          <Button size="large" type="primary" @click="handleAddEquipment">确认添加</Button>
        </FormItem>
      </Form>
    </Modal>
    <Drawer v-model="showEditScene" width="1050px">
      <div class="drawing-container">
        <div id="tui-image-editor" ></div>
      <div style="display:flex; align-items:center; justify-content:center; margin-top:20px">
        <Button type='primary' size='large' @click="handleUpdateSceneImg">更新场景图</Button>
      </div>
      </div>
    </Drawer>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios'
import "tui-image-editor/dist/tui-image-editor.css";
import "tui-color-picker/dist/tui-color-picker.css";
import ImageEditor from "tui-image-editor";
export default {
  name: "SceneTable",
  props: {
    sceneData: [],
  },
  data() {
    return {
      instance: null,
      showEquipmentInfo: false,
      showAddEquipment: false,
      showEditScene: false,
      showEditEquipment: false,
      certainEquipment: {
        id: null,
        name: "",
        state: null,
        type: ""
      },
      columns: [
        {
          title: "场景编号",
          key: "sceneNo",
          width: 93,
        },
        {
          title: "场景名称",
          key: "sceneName",
          width: 180,
        },
        {
          title: "场景设备",
          key: "equipments",
        },
        {
          title: "场景户型图",
          key: "image",
          render: (h, params) => {
            return h("img", {
              attrs: {
                src: this.sceneData[params.index].oriImage
              },
              style:{
                width: "200px",
                height: "200px"
              }
            })
          }
        },
        {
          title: "可执行操作",
          key: "actions",
          render: (h, params) => {
            return h("div", [
              h(
                'Button',
                {
                  props: {
                    type: "primary",
                    size: "small",
                  },
                  on: {
                    click: () => {
                      this.showEquipmentInfo = true
                      this.equipmentData = this.sceneData[params.index].equipments
                      console.log(this.equipmentData)
                    }
                  },
                  style: {
                    margin: "5px",
                  },
                }, '查看设备信息'
              ),
              h(
                'Button',
                {
                  props: {
                    type: "primary",
                    size: "small",
                  },
                  style: {
                    margin: "5px",
                  },
                  on: {
                    click: () => {
                      this.showAddEquipment = true
                      this.equipToAddData.sceneNo = this.sceneData[params.index].sceneNo
                    }
                  }
                }, '添加智能设备'
              ),
              h(
                'Button',
                {
                  props: {
                    type: "primary",
                    size: "small",
                  },
                  style: {
                    margin: "5px",
                  },
                  on: {
                    click: () => {
                      this.showEditScene = true
                      this.sceneImgToEdit = this.sceneData[params.index].oriImage
                      this.sceneImgToEditId = this.sceneData[params.index].sceneNo
                      this.init()
                    }
                  }
                }, '编辑场景图'
              ),
            ]);
          },
        },
      ],
      equipToAddData: {
        name: "",
        type: "",
        state: null,
        sceneNo: null,
      },
      sceneImgToEdit: "",
      // sceneData: [
      //   {
      //     sceneNo: 1,
      //     sceneName: 'kitchen',
      //     equipments: [
      //       {
      //         no: 1,
      //         type: 1,
      //         name: 'lamp',
      //         state: 0,
      //       }
      //     ]
      //   }
      // ],
      equipmentColumns: [
        {
          title: '设备编号',
          key: 'id',
          width: 93,
        },
        {
          title: '设备名称',
          key: 'name',
          width: 180,
        },
        {
          title: '设备类型',
          key: 'type',
          width: 93,
        },
        {
          title: '设备状态',
          key: 'state',
          width: 93,
        },
        {
          title: '更改设备信息',
          key: 'action',
          render: (h, params) => {
            return h("div", [
              h(
                'Button',
                {
                  props: {
                    type: "primary",
                    size: "small",
                  },
                  on: {
                    click: () => {
                      this.showEditEquipment = true
                      this.certainEquipment = this.equipmentData[params.index]
                    }
                  },
                  style: {
                    margin: "5px",
                  },
                }, '上报信息'),
                h(
                'Button',
                {
                  props: {
                    type: "error",
                    size: "small",
                  },
                  on: {
                    click: () => {
                      let equipNo = this.equipmentData[params.index].id
                      axios.post('http://127.0.0.1:8000/scene/equip/delete', equipNo)
                      .then(() => {
                        this.$Message['success']({background: true, content: '删除'+equipNo+'号设备成功！'})
                      })
                      this.equipmentData.splice(params.index, 1)
                    }
                  },
                  style: {
                    margin: "5px",
                  },
                }, '删除设备')
              ])
            }
        }
      ],
      equipmentData: [],
      equipmentType: [
        { key: 1, name: "灯"},
        { key: 2, name: "温度计"},
        { key: 3, name: "湿度计" },
        { key: 4, name: "门锁"},
        { key: 5, name: "开关"},
      ]
    }
  },
  methods: {
    handleEditEquipment() {
      axios.post("http://127.0.0.1:8000/scene/equip/edit", this.certainEquipment)
      .then((res) => {
        let state = res.data.state
        if (state == 1) {
          this.$Message['error']({background: true, content:"设备信息上报失败！"})
          return ;
        }
        this.$Message['success']({background: true, content:"设备信息上报成功！"})
        this.showEditEquipment = false
      })
      for (let i = 0; i < this.equipmentData.length; i++) {
        if (this.equipmentData[i].id === this.certainEquipment.id) {
          this.equipmentData[i] = this.certainEquipment
          break
        }
      }
    },
    handleAddEquipment() {
      console.log(this.equipToAddData)
      axios.post('http://127.0.0.1:8000/scene/equip/add', this.equipToAddData)
      .then(res=>{
        console.log(res.data)
        let state = res.data.state
        if (state == 1) {
          this.$Message['warning']({background: true, content:"设备名称重复! "})
        } else {
          for (let i = 0; i < this.sceneData.length; i++) {
            if (this.sceneData[i].sceneNo === this.equipToAddData.sceneNo) {
              this.sceneData[i].equipments = res.data.equipments
              break
            }
          }
          this.$Message['success']({background: true, content:"设备添加成功! "})
          this.showAddEquipment = false
          this.equipToAddData.name = ""
          this.equipToAddData.type = null
          this.equipToAddData.state = null
        }
      })
    },
    transEquipType(key) {
      if (key == 1) {
        return "灯"
      } else if (key == 2) {
        return "温度计"
      } else if (key == 3) {
        return "湿度计"
      } else if (key == 4) {
        return "门锁"
      } else if (key == 5) {
        return "开关"
      }
    },
    init() {
      this.instance = new ImageEditor(
        document.querySelector("#tui-image-editor"),
        {
          includeUI: {
            loadImage: {
              path: this.sceneImgToEdit,
              name: "image",
            },
            initMenu: "draw", // 默认打开的菜单项
            menuBarPosition: "bottom", // 菜单所在的位置,
            theme: customTheme,
          },
          cssMaxWidth: 800, // canvas 最大宽度
          cssMaxHeight: 400, // canvas 最大高度
        }
      );
      // 图片距顶部工具栏的距离
      document.getElementsByClassName("tui-image-editor-main")[0].style.top = 0;
      console.log(this.sceneImgToEdit)
    },
    handleUpdateSceneImg() {
      this.$Message['info']({background: true, content: "正在转换文件格式并更新后台数据，请稍等~"})
      const base64String = this.instance.toDataURL(); // base64 文件
      const d = window.atob(base64String.split(",")[1]);
      const ia = new Uint8Array(d.length);
      for (let i = 0; i < d.length; i++) {
        ia[i] = d.charCodeAt(i);
      }
      const blob = new Blob([ia], { type: "image/jpg" }); // blob 文件
      let data = new FormData();
      data.append("image", blob);
      data.append("sceneNo", this.sceneImgToEditId)
      axios.post("http://127.0.0.1:8000/scene/edit", data)
      .then(res=>{
        this.showEditScene = false
        this.$Message['success']({background: true, content: "场景图编辑成功"})
        for (var i = 0; i < this.sceneData.length; i++) {
          if (this.sceneData[i].sceneNo === this.sceneImgToEditId) {
            this.sceneData[i].oriImage = res.data.imageUrl
            break
          }
        }
      })
    }
  },
  computed: {
    displayData: function() {
      var res = []
      for (var i = 0; i < this.sceneData.length; i++) {
        var temp = {
          equipments: "",
          sceneNo: this.sceneData[i].sceneNo,
          sceneName: this.sceneData[i].sceneName,
        }
        for (var j = 0; j < this.sceneData[i].equipments.length; j++) {
          temp.equipments += " " + this.sceneData[i].equipments[j].name
          // this.sceneData[i].equipments[j].type = this.transEquipType(this.sceneData[i].equipments[j].type)
        }
        if (temp.equipments === "") {
          temp.equipments = '暂无设备，请添加'
        }
        res.push(temp)
      }
      return res
    }
  },
  mounted() {
    this.init();
  },
};
const customTheme = {
  // image 坐上角度图片
  "common.bi.image": "https://uploadbeta.com/api/pictures/random/", // 在这里换上你喜欢的logo图片
  "common.bisize.width": "0px",
  "common.bisize.height": "0px",
  "common.backgroundImage": "none",
  "common.backgroundColor": "#f3f4f6",
  "common.border": "1px solid #444",

  // header
  "header.backgroundImage": "none",
  "header.backgroundColor": "#f3f4f6",
  "header.border": "0px",
  "header.display": "none",

  // load button
  "loadButton.backgroundColor": "#fff",
  "loadButton.border": "1px solid #ddd",
  "loadButton.color": "#222",
  "loadButton.fontFamily": "NotoSans, sans-serif",
  "loadButton.fontSize": "12px",
  "loadButton.display": "none", // 可以直接隐藏掉

  // download button
  "downloadButton.backgroundColor": "#fdba3b",
  "downloadButton.border": "1px solid #fdba3b",
  "downloadButton.color": "#fff",
  "downloadButton.fontFamily": "NotoSans, sans-serif",
  "downloadButton.fontSize": "12px",
  "downloadButton.display": "none", // 可以直接隐藏掉

  // icons default
  "menu.normalIcon.color": "#8a8a8a",
  "menu.activeIcon.color": "#555555",
  "menu.disabledIcon.color": "#434343",
  "menu.hoverIcon.color": "#e9e9e9",
  "submenu.normalIcon.color": "#8a8a8a",
  "submenu.activeIcon.color": "#e9e9e9",

  "menu.iconSize.width": "24px",
  "menu.iconSize.height": "24px",
  "submenu.iconSize.width": "32px",
  "submenu.iconSize.height": "32px",

  // submenu primary color
  "submenu.backgroundColor": "#1e1e1e",
  "submenu.partition.color": "#858585",

  // submenu labels
  "submenu.normalLabel.color": "#858585",
  "submenu.normalLabel.fontWeight": "lighter",
  "submenu.activeLabel.color": "#fff",
  "submenu.activeLabel.fontWeight": "lighter",

  // checkbox style
  "checkbox.border": "1px solid #ccc",
  "checkbox.backgroundColor": "#fff",

  // rango style
  "range.pointer.color": "#fff",
  "range.bar.color": "#666",
  "range.subbar.color": "#d1d1d1",

  "range.disabledPointer.color": "#414141",
  "range.disabledBar.color": "#282828",
  "range.disabledSubbar.color": "#414141",

  "range.value.color": "#fff",
  "range.value.fontWeight": "lighter",
  "range.value.fontSize": "11px",
  "range.value.border": "1px solid #353535",
  "range.value.backgroundColor": "#151515",
  "range.title.color": "#fff",
  "range.title.fontWeight": "lighter",

  // colorpicker style
  "colorpicker.button.border": "1px solid #1e1e1e",
  "colorpicker.title.color": "#fff",
};
</script>

<style scoped>
.drawing-container {
  height: 700px;
  width: 1000px;
}
</style>
