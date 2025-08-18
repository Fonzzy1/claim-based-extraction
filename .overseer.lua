return {
    {
        name = "Update Dataset",
        builder = function(_)
            local cmd_str = table.concat({
                "pip install -r requirements.txt",
                "prisma generate",
                "python3 update.py",
            }, " && ")
            return {
                cwd = "database",
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Update Dataset'
            }
        end,
    },
    {
        name = "Update Database",
        builder = function(_)
            local cmd_str = table.concat({
                "pip install prisma",
                "prisma migrate dev"
            }, " && ")
            return {
                cwd = "database",
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Update Database Structure'
            }
        end,
    },
    {
        name = "Reset Database",
        builder = function(_)
            local cmd_str = table.concat({
                "pip install prisma",
                "prisma migrate dev"
            }, " && ")
            return {
                cwd = "database",
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Reset Database'
            }
        end,
    },
    {
        name = "Prisma Studio",
        builder = function(_)
            local cmd_str = table.concat({
                "pip install prisma",
                "prisma studio"
            }, " && ")
            return {
                cwd = "database",
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Prisma Studio'
            }
        end,
    }
}
