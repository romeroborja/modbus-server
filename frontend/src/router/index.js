import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/:catchAll(.*)",
    redirect: { name: '/' },
  },
  {
    path: "/",
    name: "/",
    redirect: "/modbus",
  },
  {
    path: "/modbus",
    name: "Modbus addresses",
    component: () => import('@/views/AutomaticDesign.vue'),
    meta: { auth: true }
  },
  {
    path: "/configuration",
    name: "Configuración",
    component: () => import('@/views/AutomaticDesign.vue'),
    meta: { auth: true }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active",
});

export default router;
