<template>
  <Table style="width: 100%;" stripe border :columns="columns"></Table>
</template>

<script>
/* eslint-disable */
export default {
  name: "SceneTable",
  data() {
    return {
      columns: [
        {
          title: '场景编号',
          key: 'sceneNo'
        },
        {
          title: '场景名称',
          key: 'sceneName'
        },
        {
          title: '场景设备',
          key: 'equipments'
        },
        {
          title: '可执行操作',
          key: 'actions'
        }
      ]
    };
  },
};
</script>
