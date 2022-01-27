import re
import DPyUtils
from discord.ext import commands

ks = "kwrboygpn;"
squares = dict(zip(ks, "⬛⬜🟥🟦🟧🟨🟩🟪🟫\n"))
presets = {
    "chess": "(4x(4xkw);(4xwk);)",
    "heart": """{bg}15
    {bg}4{c}2{bg}3{c}2{bg}4
    {bg}3{c}4{bg}{c}4{bg}3
    {bg}2{c}11{bg}2
    {bg}{c}13{bg}
    {bg}{c}13{bg}
    {bg}2{c}11{bg}2
    {bg}3{c}9{bg}3
    {bg}4{c}7{bg}4
    {bg}5{c}5{bg}5
    {bg}6{c}3{bg}6
    {bg}7{c}{bg}7""",
    "link": """k15
k5g6k4
k4g8k3
k2okgn6gkok
k2okn8kok
k2o2nogo2gono2k
k2o2nono2nono2k
k3o10nk
k4go2n2o2gn2k
k2n5o3g3ok
kn2on4g5ok
kno3n2on2g2nk2
kn2on3ogn3gk2
kn2on3on2g3k2
kn6og3nk3
k2o5k2n3k3
k9n3k3
k15

k10g2k3
k10gk4
ko9gngng
o10gngng
ko9gngng
k10gk4
k10g2k3""",
    "ml": """k3{cloth}5k4
k2{cloth}9k
k2{hair}3o2{hair}ok3
k{hair}o{hair}o3{hair}o3k
k{hair}o{hair}2o3{hair}o3
k{hair}2o4{hair}4k
k3o7k2
k2{hair}2{cloth}{hair}3k4
k{hair}3{cloth}{hair}2{cloth}{hair}3k
{hair}4{cloth}4{hair}4
o2{hair}{cloth}o{cloth}2o{cloth}{hair}o2
o3{cloth}6o3
o2{cloth}8o2
(2xk2{cloth}3)k2
k{hair}3k4{hair}3k
{hair}4k4{hair}4""",
    "kirby": """w18
w3k2wk5w7
w2kp2kp5k2w5
wkp2kp8kw4
(2xwkp5kpkp4kw3;)wkp5kpkp5kw2
wk(2xp3r2)p4kw
wkp6kp7kw
w2kp5kp7kw
w2kp10k3w2
w2kp9kr3kw
w3kp7kr4kw
w3k2p6kr4kw
w2kr2k2p3kr4kw2
wkr5k5r2kw3
w2k6w3k3w4
w18""",
    "triforce": "yell at clari to do this",
}


class SquareDraw(commands.Converter):
    async def preset(self, ctx: DPyUtils.Context, arg):
        lines = []
        text = ""
        if arg in ("mario", "luigi"):
            h, c = ("n", "r") if arg == "mario" else ("g", "w")
            text = presets["ml"].format(hair=h, cloth=c)
        if arg[1:] == "heart":
            c = arg[0]
            bg = "k" if c != "k" else "w"
            text = presets["heart"].format(bg=bg, c=c)
        if not text and arg not in presets:
            return
        text = text or presets.get(arg)
        for a in text.split():
            lines.append(await self.convert(ctx, a))
        return "\n".join((*lines, squares["k"] * max(map(len, lines))))

    async def convert(self, ctx: DPyUtils.Context, arg):
        if lines := (await self.preset(ctx, arg)):
            return lines
        arg = str(arg).lower()
        sec = rf"([{ks}])(\d+)?"
        primreg = re.compile(
            rf"\((\d+)x(({sec})+)\)", flags=re.IGNORECASE | re.MULTILINE
        )
        while it := list(primreg.finditer(arg)):
            for m in it:
                arg = arg.replace(m.group(0), m.group(2) * int(m.group(1)))
        reg = re.compile(sec, flags=re.IGNORECASE | re.MULTILINE)
        matches = reg.finditer(arg)
        if not matches:
            raise commands.BadArgument(f"Invalid input {arg}")
        line = ""
        for m in matches:
            k, n = m.groups()
            n = n or 1
            line += squares[k] * int(n)
        return line
