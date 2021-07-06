import backend from "@/backend";

export default {
    checkSession: async (session) => {
        if (!session){
            return null
        }

        let user = null

        await backend.checkSession(session)
            .then(res => {
                if (res.errors.length > 0){
                    return null
                }

                user = res.user
            }).catch((err) => {
                console.log(err)
            })

        return user
    },
}
