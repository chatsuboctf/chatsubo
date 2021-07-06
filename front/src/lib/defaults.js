export const defaults = {
    flag: {
        name: "",
        icon: "mdi-flag",
        value: "",
        user: false,
        root: false,
        case_insensitive: false,
        dynamic: false,
        points: 0,
        loaders: {
            generate: false
        },
        stub: true
    },
    queueState: {
        tickID: null,
        state: "",
        position: "1",
        queueLen: "-"
    },
    newBox: {
        name: "",
        description: "",
        template: undefined,
        dockerfile: "",
        authors: [],
        duration: 60,
        // background: "",
        background: "/static/img/default_box.png",
        os: "",
        kind: false,
        flags: [],
        validated_flags: [],
        category: {},
        difficulty: 0,
      }
}
