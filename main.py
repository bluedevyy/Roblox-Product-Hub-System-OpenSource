import nextcord
from nextcord.ext import commands, application_checks
from nextcord import SlashOption
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

client3 = pymongo.MongoClient(MONGOURI)
db3 = client3.data
collection3 = db3.users

intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Bot Ready!')

@bot.slash_command(name="createproduct", description="creates a product")
@application_checks.has_permissions(kick_members=True)
async def create(ctx, productname : str = SlashOption(name="productname", description="the products name", required=True), productdescription : str = SlashOption(name="productdescription", description="the products description", required=True), productid : str = SlashOption(name="productid", description="the products id", required=True), productstock : int = SlashOption(name="productstock", description="the products stock", required=True), producttag : str = SlashOption(name="producttag", description="the products tag", required=True), productlink : str = SlashOption(name="productlink", description="the products download link", required=True)):
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
                "producttag": producttag,
                "productlink": productlink
            }
        )

producttemplate = (
    {
        "guildid": 0,
        "productname": 0,
        "productdescription": 0,
        "productid": 0,
        "productstock": 0,
        "producttag": 0,
        "productlink": 0
    }
)        

@bot.slash_command(name="deleteproduct", description="deletes a product")
@application_checks.has_permissions(kick_members=True)
async def delete(ctx, productname : str = SlashOption(name="productname", description="the products name", required=True)):
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
    
    productsdata = collection.find_one({ "guildid": ctx.guild.id })

    error = nextcord.Embed(title="Error!", description="No products found please run ``/createproduct`` to create a product.")

    embed = nextcord.Embed(title=f"Products For {ctx.guild.name}", description="Products Below.").add_field(name="Products", value=f"\n".join(map(str, productsdata["productname"])), inline=False)

    if collection.count_documents({ "guildid": ctx.guild.id }):
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=error)

@bot.slash_command(name="setup", description="setups the hub")
@application_checks.has_permissions(kick_members=True)
async def setup(ctx, hubname : str = SlashOption(name="hubname", description="the hubs name", required=True), placeid : str = SlashOption(name="placeid", description="the placeid of the hub", required=True)):

    apikeygener = random.randrange(35409834590843908)

    embed = nextcord.Embed(title="Setup The Hub.", description="We're setting up your hub for your right now. you will shortly be messaged the details.")
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
                "products": []
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
        print(f"{ctx.guild.name} has no hub setup")

@bot.slash_command(name="editproduct", description="edits a product")
@application_checks.has_permissions(kick_members=True)
async def edit(ctx, currentproductname : str = SlashOption(name="currentproductname", description="the products current name", required=False), newproductname : str = SlashOption(name="newproductname", description="the products new name", required=False), newproductid : str = SlashOption(name="newproductid", description="the products new id", required=False), newproductdescription : str = SlashOption(name="newproductdescription", required=False), newproductstock : int = SlashOption(name="newproductstock", description="the products new stock", required=False), newproducttag : str = SlashOption(name="newproducttag", description="the products new tag", required=False), productlink : str = SlashOption(name="productlink", description="the products download link", required=False)):
    if collection.count_documents({ "productname": currentproductname }):
        await ctx.send('Updated product successfully.')

        ok22 = collection.find_one(
            {
                "productname": currentproductname
            }
        )

        ok = collection.update_one(
        {"productname": ok22['productname']},
        {"$set": 
            {"productname": newproductname}
        },upsert=True
    )

        ok = collection.update_one(
        {"productdescription": ok22['productdescription']},
        {"$set": 
            {"productdescription": newproductdescription}
        },upsert=True
    )

        ok = collection.update_one(
        {"productid": ok22['productid']},
        {"$set": 
            {"productdescription": newproductid}
        },upsert=True
    )

        ok = collection.update_one(
        {"productstock": ok22['productstock']},
        {"$set": 
            {"productstock": newproductstock}
        },upsert=True
    )

        ok = collection.update_one(
        {"producttag": ok22['producttag']},
        {"$set": 
            {"producttag": newproducttag}
        },upsert=True
    )

    else:
        await ctx.send("Product doesn't exist.")

collection3

@bot.slash_command(name="giveproduct", description="gives a user a product")
@application_checks.has_permissions(kick_members=True)
async def give(ctx, user : nextcord.Member, productname : str = SlashOption(name="productname", description="the products name", required=True)):
    if collection.count_documents({ "productname": productname }):

        if collection3.count_documents({ "userid": ctx.user.id }):
            await ctx.send(f'Gave {productname} to {user.name}.')
            ok = collection3.insert_one(
                {
                    "Ownedproducts": [f'{productname}'],
                }
            )
        else:
            await ctx.send(f"user isn't linked.")

    else:
        await ctx.send("product doesn't exist")

@bot.slash_command(name="link", description="links a user")
async def link(ctx, robloxusername : str = SlashOption(name="robloxusername", description="your roblox username", required=True)):
    if collection3.count_documents({ "userid": ctx.user.id }):
        await ctx.send('your already linked.')
    else:
        await ctx.send(f'linked as {robloxusername} Successfully.')
        await ctx.user.edit(nick=robloxusername)

        collection3.insert_one(
            {
                "userid": ctx.user.id,
                "robloxusername": robloxusername,
                "Ownedproducts": ['none'],
                "linked": True,
                "HasCustomBot": False,
            }
        )


@bot.slash_command(name="profile", description="sends a users profile")
async def profile(ctx, user : nextcord.Member = SlashOption(name="user", description="the users profile you want to view.", required=False)):

    data = collection3.find_one(
        {
            "userid": user.id
        }
    )

    embed = nextcord.Embed(title=f"Profile Of {user.name}", description=f"DiscordID:\n{user.id}\nRobloxusername:\n{data['robloxusername']}").add_field(name="OwnedProducts", value=f"\n".join(map(str, data['Ownedproducts'])))
    if collection3.count_documents({ "userid": user.id }):
        await ctx.send(embed=embed)
    else: 
        await ctx.send("User isn't linked.")

@bot.slash_command(name="unlink", description="unlinks your roblox account")
async def unlink(ctx):
    if collection3.count_documents({ "userid": ctx.user.id }):
        await ctx.send('Unlinked successfully.')
        collection3.delete_one(
            {
                "userid": ctx.user.id
            }
        )
    else:
        await ctx.send('Your not linked.')

@bot.slash_command(name="ping", description="the bots ping")
async def ping(ctx):
    await ctx.send(f'bot ping: **{bot.latency*100:,.0f} ms**')

# retrievetemplate = nextcord.Embed(title="Thanks For Purchasing!", description="Thanks For Purchasing A Product From us. the product is below.")
# retrievetemplate.add_field(name="DownloadLink": value=f"Link", inline=False)

@bot.slash_command(name="retrieveproduct", description="retrieves a product")
async def retrieve(ctx, productname : str = SlashOption(name="productname", description="the products name", required=True)):
    embederror = nextcord.Embed(title="You do not own this product.", description="you don't own this product.")
    if collection3.count_documents({ "Ownedproducts": [productname] }):

        productsclientdata = collection.find_one(
            {
                "productname": productname,
            }
        )

        embed = nextcord.Embed(title="Thanks For Purchasing!", description=f"Thanks For Purchasing A Product From us. the product is below.\n Downloadlink: {productsclientdata['productlink']}")
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=embederror)

@bot.slash_command(name="revokeproduct", description="revokes a product")
async def revoke(ctx, user : nextcord.Member = SlashOption(name="user", description="the user you want revoke a product from.", required=True), productname : str = SlashOption(name="productname", description="the products name", required=True)):
    if collection3.count_documents({ "userid": user.id, "Ownedproducts": [f'{productname}'] }):
        await ctx.send(f"revoked {productname} from {user.name}")
    else:
        await ctx.send("User doesn't own that product. or user doesn't exist.")

@bot.slash_command(name="transferdata", description="transfers users data to another account.")
async def transfer(ctx, newaccount : nextcord.Member = SlashOption(name="newaccount", description="the new account to transfer data to.", required=True)):
    if collection3.count_documents({ "userid": ctx.user.id }):
        await ctx.send('Transferred data succecssfully.')
        
    else:
        await ctx.send("Couldn't transfer data maybe because the user isn't linked.")

bot.run(TOKEN)