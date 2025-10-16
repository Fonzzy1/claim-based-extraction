from prisma import Client
from models.filter import Filter

#
db = Client()
await db.connect()

filter = Filter.load_from_gd('basic_filter')

documents = await db.document.find_many()

filtered_documents = [x for x in documents if filter.infer(x)]


