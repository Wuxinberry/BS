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
    <Drawer v-model="showEditScene" width="1100px">
      <div class="drawing-container">
        <div id="tui-image-editor"></div>
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
              name: "场景图",
            },
            initMenu: "draw", // 默认打开的菜单项
            menuBarPosition: "bottom", // 菜单所在的位置
          },
          cssMaxWidth: 800, // canvas 最大宽度
          cssMaxHeight: 400, // canvas 最大高度
        }
      );
      document.getElementsByClassName("tui-image-editor-main")[0].style.top = "45px"; // 图片距顶部工具栏的距离
      
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
        res.push(temp)
      }
      return res
    }
  },
  mounted() {
    this.init()
  }
};
</script>

<style scoped>
.drawing-container {
  height: 700px;
  width: 1000px;
}
</style>
