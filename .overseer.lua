return {
    {
        name = "Docker Compose Up",
        builder = function(_)
            local cmd_str = "sh run.sh up"
            return {
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Update Dataset'
            }
        end,
    },
    {
        name = "Docker Compose Down",
        builder = function(_)
            local cmd_str = "sh run.sh down"
            return {
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Update Dataset'
            }
        end,
    },
    {
        name = "Docker Compose Logs",
        builder = function(_)
            local cmd_str = "sh run.sh logs"
            return {
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Update Dataset'
            }
        end,
    },
}
