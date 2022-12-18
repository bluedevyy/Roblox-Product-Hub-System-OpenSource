import nextcord
from nextcord.ext import commands, application_checks
import pymongo

MONGOURI = "mongodb+srv://Blue:Blue@sustain.ghwzh3l.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGOURI)
db = client.data
collection = db.products

client2 = pymongo.MongoClient(MONGOURI)
db2 = client2.data
collection2 = db2.hub

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Bot Ready!')

@bot.slash_command(name="createproduct", description="creates a product")
async def create(ctx, productname : str, productdescription : str, productid : str, productstock : int, producttag : str):
    if collection.count_documents({"productname": productname}):
        await ctx.send('a product with that name already exists.')
    else:
        await ctx.send('created product successfully.')
        collection.insert_one(
            {
                "guildid": ctx.guild.id,
                "productname": productname,
                "productdescription": productdescription,
                "productid": productid,
                "productstock": productstock,
                "producttag": producttag
            }
        )

@bot.slash_command(name="deleteproduct", description="deletes a product")
async def delete(ctx, productname : str):
    if collection.count_documents({"productname": productname}):
        await ctx.send('product deleted successfully.')
        collection.delete_one(
            {
                "productname": productname
            }
        )
    else:
        await ctx.send("product doesn't exist.")

@bot.slash_command(name="products", description="sends the products that exist")
async def products(ctx):

    productsdata = collection.find({ "guildid": ctx.guild.id })

    error = nextcord.Embed(title="Error!", description="No products found please run ``/createproduct`` to create a product.")

    embed = nextcord.Embed(title=f"Products For {ctx.guild.name}", description="\n".join(productsdata['productname']))

    if collection.count_documents({ "guildid": ctx.guild.id }):
        ctx.send(embed=embed)
    else:
        ctx.send(embed=error)

@bot.slash_command(name="setup", description="setups the hub")
async def setup(ctx, hubname : str, placeid : str):

    embed = nextcord.Embed(title="")

    if collection2.count_documents({ "guildid": ctx.guild.id }):
        await ctx.send('Hub is already setup.')
    else:
        await ctx.send(embed=embed)

@bot.slash_command(name="hub", description="sends the data of the hub.")
async def hub(ctx):



    await ctx.send(embed=embed)


bot.run('ODkzOTI3MzcxOTg2NTcxMzA2.G7WCrc.kAuu6wJ8VUJtLcU5TgZvkqda-PmcZFoMbF7_RU')