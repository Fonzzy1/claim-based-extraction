return {
    {
        name = "Update Hansard",
        builder = function(_)
            local cmd_str = table.concat({
                "pip install prisma lxml wget",
                "prisma generate",
                "python3 scrapers/scrapers/hansard.py ",
                "python3 scrapers/parsers/hansard.py "
            }, " && ")
            return {
                cwd = "database",
                cmd = { "sh", "-c", cmd_str },
                components = { "default" },
                name = 'Update Hansard'
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
