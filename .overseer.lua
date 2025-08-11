return {
    {
        name = "Update Dataset",
        builder = function(_)
            local cmd_str = table.concat({
                "pip install prisma lxml wget fuzzywuzzy",
                "prisma generate",
                "python3 scrapers/hansard.py ",
                "python3 scrapers/politicians.py ",
                "python3 parsers/hansard.py ",
                "python3 parsers/politicians.py "
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
