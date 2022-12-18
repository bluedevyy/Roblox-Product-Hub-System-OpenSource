import nextcord
from nextcord.ext import commands, application_checks
import pymongo
import random

MONGOURI = ""
TOKEN = ""

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
@application_checks.has_permissions(kick_members=True)
async def setup(ctx, hubname : str, placeid : str):

    apikeygener = random.randrange(35409834590843908)

    embed = nextcord.Embed(title="setup", description="We're setting up your hub for your right now. you will shortly be messaged the details.")
    error = nextcord.Embed(title="Error", description="Hub is already setup")

    if collection2.count_documents({ "guildid": ctx.guild.id }):
        await ctx.send(embed=error)
    else:
        await ctx.send(embed=embed)

        collection2.insert_one(
            {
                "guildid": ctx.guild.id,
                "customhub": False,
                "apikey": apikeygener,
                "placeid": placeid,
                "hubname": hubname,
            }
        )

        data11 = collection2.find_one(
            {
                "guildid": ctx.guild.id
            }
        )

        await ctx.user.send(f"apikey: {data11['apikey']}, hubname: {data11['hubname']}, customhub: {data11['customhub']}")

@bot.slash_command(name="hub", description="sends the data of the hub.")
async def hub(ctx):

    data = collection2.find_one(
        {
            "guildid": ctx.guild.id
        }
    )

    embed = nextcord.Embed(title=f"Hub Information", description=f"customhub: {data['customhub']}\n\nplaceid: {data['placeid']}\n\\napikey: {data['apikey']}\n\n hubname: {data['hubname']}")

    if collection2.count_documents({ "guildid": ctx.guild.id }):
        await ctx.send(embed=embed)
    else:
        await ctx.send("this guild doesn't have a hub.")


bot.run(TOKEN)