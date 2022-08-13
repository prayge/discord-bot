users_df = pd.read_sql(
    f"select phrase from phrases where username = 'Keito'", connection)
links = users_df[users_df["phrase"].str.contains('http')]
print(links)
list_links = links.to_dict('list')
links = list_links["phrase"]

frame_df = pd.read_sql(
    f"select phrase from phrases where username = 'frame'", connection)
frame = frame_df[frame_df["phrase"].str.contains('http')]
list_frame = frame.to_dict('list')
frame = list_frame["phrase"]

rand_frame = requests.get(random.choice(frame))
response = requests.get(random.choice(links))
print("d")
with Image.open(BytesIO(response.content)) as im:
    print("e")
    w, h = im.size

    im2 = Image.open(BytesIO(rand_frame.content))

    im.paste(im2, (0, 0), im2)

    print("saving")
    im.save("test.png")
    await ctx.send(file=discord.File('test.png'))
