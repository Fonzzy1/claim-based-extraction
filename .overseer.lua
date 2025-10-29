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
    {
        name = "Generate Synthetic Data for Semantic Filter",
        builder = function(_)
            local cmd_str = "PYTHONPATH=$(pwd) python3 ./data/synthetic/semantic_filter/generate_data.py"
            return {
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Generate Data in for the Semantic Filter'
            }
        end,
    },
}
