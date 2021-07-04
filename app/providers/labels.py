def parse_flags(labels):
    flags = {}
    for label, val in labels.items():
        if label.startswith("chatsubo.flags."):
            data = label[len("chatsubo.flags."):]
            if "." not in data:
                # malformed flag label
                # ex : chatsubo.flags.the_flag.value=flag{1234abcd...}
                continue
            chunks = data.split(".", maxsplit=1)
            name = chunks[0]
            data_type = chunks[1]
            if name in flags:
                flags[name][data_type] = val
            else:
                flags[name] = {
                    data_type: val
                }

    return [{"name": name, "value": flag["value"], "points": flag["points"]} for name, flag in flags.items() if "value" in flag and flag.get("points")]


def parse_creds(labels):
    creds = {}
    for label, val in labels.items():
        if label.startswith("chatsubo.creds."):
            data = label[len("chatsubo.creds."):]
            if "." not in data:
                # malformed flag label
                # ex : chatsubo.creds.ssh.username=user1
                continue
            chunks = data.split(".", maxsplit=1)
            creds_type = chunks[0]
            data_type = chunks[1]
            if creds_type in creds:
                creds[creds_type][data_type] = val
            else:
                creds[creds_type] = {
                    data_type: val
                }
    return [
        {
            "type": creds_type,
            "username": access["username"],
            "password": access["password"]
        }
        for creds_type, access in creds.items()
    ]
