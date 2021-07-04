import Vue from 'vue'
import Router from 'vue-router'
import Container from '@/views/Container.vue'
import Login from "@/views/auth/Login"
import Home from "@/views/Home"
import Logout from "@/views/auth/Logout"
// import Profile from "@/views/Profile"
import AdminBoxes from "@/views/admin/AdminBoxes";
import Passthrough from "@/views/Passthrough";
import AdminCategories from "@/views/admin/AdminCategories";
import AdminBoxProfile from "@/views/admin/AdminBoxProfile";
import Scoreboard from "@/views/Scoreboard";
import Tracks from "@/views/Tracks";
import BoxProfile from "@/views/BoxProfile";
import Users from "@/views/Users";
import Teams from "@/views/Teams";
import Team from "@/views/Team";
import Settings from "@/views/Settings";
import Submissions from "@/views/Submissions";
import AdminSettings from "@/views/admin/AdminSettings";

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Container,
      redirect: "home",
      children: [
        {
          path: 'home',
          name: 'home',
          component: Home,
          meta: {
            requireAuth: true,
            title: "Home"
          }
        },
        {
          path: 'scoreboard',
          name: 'scoreboard',
          component: Scoreboard,
          meta: {
            requireAuth: true,
            title: "Scoreboard"
          }
        },
        {
          path: 'users',
          name: 'users',
          component: Users,
          meta: {
            requireAuth: true,
            title: "Users"
          }
        },
        {
          path: 'teams',
          name: 'teams',
          component: Teams,
          meta: {
            requireAuth: true,
            title: "Teams"
          }
        },
        {
          path: 'team',
          name: 'team',
          component: Team,
          meta: {
            requireAuth: true,
            title: "Team"
          }
        },
        // {
        //   path: 'team',
        //   name: 'teamCatch',
        //   redirect: 'team/self',
        //   meta: {
        //     requireAuth: true,
        //   }
        // },
        {
          path: 'team/:who',
          name: 'team',
          component: Team,
          meta: {
            requireAuth: true,
            title: "Team"
          }
        },
        {
          path: 'settings',
          name: 'settings',
          component: Settings,
          meta: {
            requireAuth: true,
            title: "Settings"
          }
        },
        // {
        //   path: 'profile',
        //   name: 'profileCatch',
        //   redirect: 'profile/self',
        //   meta: {
        //     requireAuth: true,
        //   }
        // },
        // {
        //   path: 'profile/:who',
        //   name: 'profile',
        //   component: Profile,
        //   meta: {
        //     requireAuth: true,
        //     title: "Profile"
        //   }
        // },
        {
          path: 'tracks/:category',
          name: 'Tracks',
          component: Tracks,
          meta: {
            requireAuth: true,
            title: "Tracks"
          }
        },
        {
          path: 'box/:box',
          name: 'box',
          component: BoxProfile,
          meta: {
            requireAuth: true,
            title: "Box"
          }
        },
        {
          path: 'admin',
          name: 'admin',
          component: Passthrough,
          redirect: "admin/boxes",
          meta: {
            requireAuth: true,
            requireAdmin: true,
            title: "Administration",
          },
          children:[
            {
              path: 'boxes',
              name: 'boxes',
              component: AdminBoxes,
              meta: {
                requireAuth: true,
                requireAdmin: true,
                title: "Boxes"
              }
            },
            {
              path: 'box/:id',
              name: 'box',
              component: AdminBoxProfile,
              meta: {
                requireAuth: true,
                requireAdmin: true,
                title: "Box",
                crumbLink: "/admin/boxes"
              }
            },
            {
              path: 'tracks',
              name: 'tracks',
              component: AdminCategories,
              meta: {
                requireAuth: true,
                requireAdmin: true,
                title: "Tracks"
              }
            },
            {
              path: 'submissions',
              name: 'submissions',
              component: Submissions,
              meta: {
                requireAuth: true,
                requireAdmin: true,
                title: "Submissions"
              }
            },
            {
              path: 'settings/:tab?',
              name: 'settings',
              component: AdminSettings,
              meta: {
                requireAuth: true,
                requireAdmin: true,
                title: "AdminSettings"
              }
            }
          ]
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      alias: ["/register"]
    },
    {
      name: 'logout',
      path: '/logout',
      component: Logout
    }
  ]
})
