import backend from "@/backend";

export default {
    fetchSettings: async () => {
        let settings = null

        await backend.fetchSettings()
            .then(res => {
                if (res.data.errors.length > 0){
                    return null
                }

                settings = res.data.data.settings
            }).catch((err) => {
                if ([404, 500].includes(err.response.status)){
                    return null
                }
                console.log(err)
            })

        return settings
    }
}
