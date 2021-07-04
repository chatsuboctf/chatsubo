import axios from 'axios'

let $axios = axios.create({
  baseURL: '/api/',
  timeout: 300000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Response Interceptor to handle and log errors
$axios.interceptors.response.use(function (response) {
  return response
}, function (error) {
  // Handle Error
  console.log(error)
  return Promise.reject(error)
})

export default {
  login(form) {
    return $axios.post(`/auth/login`, form)
        .then(response => response)
  },
  logout(user) {
    return $axios.post(`/auth/logout`, user)
        .then(response => response.data)
  },
  register(form) {
    return $axios.post(`/auth/register`, form)
        .then(response => response.data)
  },
  checkSession(session){
    return $axios.post(`/auth/check`, {session: session})
        .then(response => response.data)
  },
  getUser(username){
    return $axios.get(`/users/${username}`)
        .then(response => response)
  },
  listAllTopUsers(n){
    return $axios.get(`/users/top/${n}`)
        .then(response => response.data)
  },
  listTopUsers(data){
    return $axios.get(`/users/top/${data.n}?cat=${data.category_id}`)
        .then(response => response.data)
  },
  listUsers(){
    return $axios.get(`/users/all`)
        .then(response => response.data)
  },
  listAvailableTemplates(){
    return $axios.get(`/boxes/templates/list`)
        .then(response => response)
  },
  listBoxes(){
    return $axios.get(`/boxes/list`)
        .then(response => response.data)
  },
  getBox(name){
    return $axios.get(`/boxes/get/${name}`)
        .then(response => response)
  },
  listCategories(){
    return $axios.get(`/categories/list`)
        .then(response => response.data)
  },
  loadCategory(category_id){
    return $axios.get(`/categories/get/${category_id}`)
        .then(response => response)
  },
  loadBoxesOf(category_id){
    return $axios.get(`/boxes/list_by_category/${category_id}`)
        .then(response => response)
  },
  createNewCategory(category){
    return $axios.post(`/categories/new`, category)
        .then(response => response)
  },
  deleteCategory(category){
    return $axios.post(`/categories/delete`, category)
        .then(response => response)
  },
  restoreCategory(category){
    return $axios.post(`/categories/restore`, category)
        .then(response => response)
  },
  deleteBulkCategories(categories){
    return $axios.post(`/categories/bulk_delete`, categories)
        .then(response => response)
  },
  editCategory(category){
    return $axios.post(`/categories/edit/${category.id}`, category)
        .then(response => response)
  },
  createNewBox(box){
    return $axios.post(`/boxes/new`, box)
        .then(response => response)
  },
  deleteBox(id){
    return $axios.delete(`/boxes/delete/${id}`)
        .then(response => response)
  },
  restoreBox(box){
    return $axios.post(`/boxes/restore`, box)
        .then(response => response)
  },
  askReset(data){
    return $axios.post(`/boxes/reset/${data.realm}/${data.box.id}`, {
          user: data.user,
          session: data.session
        }
    ).then(response => response)
  },
  deleteBulkBoxes(boxes){
    return $axios.post(`/boxes/bulk_delete`, boxes)
        .then(response => response)
  },
  editBox(box){
    return $axios.post(`/boxes/edit/${box.id}`, box)
        .then(response => response)
  },
  releaseBox(box){
    return $axios.post(`/boxes/release/${box.id}`)
        .then(response => response)
  },
  retireBox(box){
    return $axios.post(`/boxes/retire/${box.id}`)
        .then(response => response)
  },
  deleteFlag(id){
    return $axios.delete(`/flags/delete/${id}`)
        .then(response => response.data)
  },
  restoreFlag(id){
    return $axios.post(`/flags/restore/${id}`)
        .then(response => response)
  },
  checkFlag(data){
    return $axios.post(`/flags/check/${data.box_id}`, data)
        .then(response => response)
  },
  generateFlag(){
    return $axios.get(`/flags/generate`)
        .then(response => response.data)
  },
  getRealms(){
    return $axios.get(`/realms/all`)
        .then(response => response)
  },
  getRealmsFor(id){
    return $axios.get(`/realms/${id}`)
        .then(response => response)
  },
  getVPNAccessFor(data){
    return $axios.get(`/vpn/get/${data.realm}/${data.username}`)
        .then(response => response)
  },
  getBoxAccess(data){
    return $axios.get(`/boxes/access/${data.realm}/${data.boxName}`)
        .then(response => response)
  },
  getBoxSession(data){
    return $axios.get(`/boxes/session/${data.realm}/${data.boxName}/${data.user.id}`)
        .then(response => response)
  },
  listTeams(){
    return $axios.get(`/teams/all`)
        .then(response => response)
  },
  joinTeam(data){
    return $axios.post(`/teams/join/${data.team.name}`, data)
        .then(response => response)
  },
  createTeam(data){
    return $axios.post(`/teams/new`, data)
        .then(response => response)
  },
  getTeam(id){
    return $axios.get(`/teams/${id}`)
        .then(response => response)
  },
  startBox(data){
    return $axios.post(`/boxes/start/${data.realm}/${data.box.id}`, data.user)
        .then(response => response)
  },
  stopBox(data){
    return $axios.post(`/boxes/stop/${data.session.id}`)
        .then(response => response)
  },
  editTeam(team){
    return $axios.post(`/teams/edit/${team.id}`, team)
        .then(response => response)
  },
  disbandTeam(team){
    return $axios.post(`/teams/disband/${team.id}`)
        .then(response => response)
  },
  leaveTeam(){
    return $axios.post(`/teams/leave`)
        .then(response => response)
  },
  editUser(user){
    return $axios.post(`/users/edit/${user.id}`, user)
        .then(response => response)
  },
  resetUserPassword(data){
    return $axios.post(`/users/reset/${data.userID}`, {"newPass": data.newPass})
        .then(response => response)
  },
  setAdmin(data){
    return $axios.post(`/users/set_admin`, data)
        .then(response => response)
  },
  editUserSelf(user){
    return $axios.post(`/users/edit`, user)
        .then(response => response)
  },
  listSubmissions(){
    return $axios.get(`/flags/submissions/all`)
        .then(response => response)
  },
  listSubmissionsForCurrentUser(userID){
    return $axios.get(`/flags/submissions/by_user/${userID}`)
        .then(response => response)
  },
  fetchSettings(){
    return $axios.get(`/settings/all`)
        .then(response => response)
  },
  editAccessSettings(accessSettings){
    return $axios.post(`/settings/access`, accessSettings)
        .then(response => response)
  },
  editGameSettings(gameSettings){
    return $axios.post(`/settings/game`, gameSettings)
        .then(response => response)
  },
  fetchQueueState(taskID){
    return $axios.get(`/queue/${taskID}`)
        .then(response => response)
  },
  uploadAvatar(data){
    let form = new FormData()
    form.append('avatar', data.avatar)

    return $axios.post(`/users/avatar/${data.userID}`, form, {headers: {'Content-Type': 'multipart/form-data'}})
  },
  uploadLogo(img){
    let form = new FormData()
    form.append('logo', img)

    return $axios.post(`/settings/logo/picture`, form, {headers: {'Content-Type': 'multipart/form-data'}})
  },
  uploadTeamAvatar(data){
    let form = new FormData()
    form.append('avatar', data.avatar)

    return $axios.post(`/teams/avatar/${data.teamID}`, form, {headers: {'Content-Type': 'multipart/form-data'}})
  },
  uploadBoxBackground(data){
    let form = new FormData()
    form.append('background', data.background)

    return $axios.post(`/boxes/background/${data.boxID}`, form, {headers: {'Content-Type': 'multipart/form-data'}})
  },
  saveLogoSizing(data){
    return $axios.post(`/settings/logo/sizing`, data)
  },
  saveHomePage(content){
    return $axios.post(`/settings/homepage`, {
      "content": content
    })
  }
}
