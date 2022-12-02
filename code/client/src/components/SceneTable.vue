<template>
  <Table style="width: 100%" stripe border :columns="columns" :data='sceneData'></Table>
</template>

<script>
/* eslint-disable */
export default {
  name: "SceneTable",
  data() {
    return {
      columns: [
        {
          title: "场景编号",
          key: "sceneNo",
        },
        {
          title: "场景名称",
          key: "sceneName",
        },
        {
          title: "场景设备",
          key: "equipments",
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
                      console.log(this.sceneData[params.index])
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
                }, '编辑场景图'
              ),
            ]);
          },
        },
      ],
      displayData: [],
      sceneData: [
        {
          sceneNo: 1,
          sceneName: 'kitchen',
          equipments: [
            {
              type: 1,
              name: 'lamp',
              state: 0,
            }
          ]
        }
      ]
    };
  },
};
</script>
