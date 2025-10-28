return {
    {
        name = "Docker Compose Up",
        builder = function(_)
            local cmd_str = "source run.sh; dc up"
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
            local cmd_str = "source run.sh; dc down"
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
            local cmd_str = "source run.sh; dc logs"
            return {
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Update Dataset'
            }
        end,

    }, {
    name = "Generate Yaml Schema",
    builder = function(_)
        local cmd_str = "PYTHONPATH=$(pwd) python3 ./experiments/configs/.schema_generator.py"
        return {
            cmd = { "sh", "-c", cmd_str },
            components = { "default" },
            name = 'Create Yaml Schema for Configs'
        }
    end,
},
}
