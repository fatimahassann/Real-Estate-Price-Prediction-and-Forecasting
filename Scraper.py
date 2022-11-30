import requests
import xlsxwriter
from bs4 import BeautifulSoup
arr = []
arr1 = []
arr2 = []
final = []
final1 = []
final2 = []
final3 = []
final4 = []
F = []
R = []
B = []
Fi = []
L = []
PPM = []
P = []
Bu = []
V = []
S = []
Se = []
Pa = []
M = []
Pu = []

f = 0
r = 0
b = 0
fi = 0
l = 0
ppm = 0
p = 0
bu = 0
v = 0
s = 0
se = 0
pa = 0
m = 0
pu = 0


#for i in range(200):
   # f'''https://aqarmap.com.eg/en/for-sale/property-type/cairo/mokattam/compounds/uptown-cairo/?minPrice={1750000}&maxPrice={8000000}&default=1'''


#listOfFilters = {'compound', 'villa', 'duplex'}

#for filter in ListOfFilters:


money = [3000001, 3500000, 3500001, 4000000, 4000001, 4500000]
money2 = [4500001, 5000000, 5000001, 5500000, 5500001, 6000000]
money3 = [6000001, 6500000, 6500001, 7000000, 7000001, 7500000]
money4 = [7500001, 8000000, 8500000, 8500001, 9000000, 9500000]
money5 = [9500001, 10000000]

address = []
compound = []
compound2 = []
typef = []
typef2 = []

#for i in range(len(money4) - 2):
page = 1
while page != 13:
    #url = f"https://aqarmap.com.eg/en/for-sale/apartment/cairo/el-sheikh-zayed-city/?minPrice={money4[i]}&maxPrice={money4[i+1]}&page={page}"
    url = f"https://aqarmap.com.eg/en/for-sale/apartment/cairo/mokattam/?minPrice=1500000&page={page}"
        #https://aqarmap.com.eg/en/for-sale/villa/cairo/new-cairo/?minPrice=2250000&maxPrice=4000000


    req = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"})
    soup = BeautifulSoup(req.content, "html.parser")
    tags = soup.find_all("a", href=True)
    for item in tags:
        if item['href'][0:11] == "/en/listing" and not item['href'] == "/en/listing/initialize":
            arr.append(item['href'])
    page = page + 1

for ar in arr:

    url = f"https://aqarmap.com.eg{ar}"
    req = requests.get(url, headers={
                       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"})
    soup = BeautifulSoup(req.content, "html.parser")
    tags6 = soup.find_all("h1")
    tags5 = soup.find_all("div", class_="listing-details-page__title-section__sub")
    tags1 = soup.find_all("li")
    tags10 = soup.find_all("p", class_="listing-details-page__title-section__address m-0")
    tags11 = soup.find_all("h3", class_="section-title__header")

    for items in tags1:
        calls = items.find_all("span", class_="col-md-3 col-5")
        tags2 = items.find_all("span", class_="count badge badge-default")
        for call in calls:
            arr1.append(call.text)
        for tagg in tags2:
            arr2.append(tagg.text)

    for ite in tags5:
        caller = ite.find("span")
        typef.append(caller.text)

    for itee in tags10:
        trippy = itee.find("a")
        address.append(trippy.text)

    for frog in tags11:
        if frog is not None:
            compound.append(frog.text)
        else:
            compound.append("")

sub1 = " M²"
sub2 = " EGP/M²"
sub3 = " EGP"

for arrrr in arr2:
    final.append(arrrr.strip())

for aa in final:
    final1.append(aa.replace(sub1, ""))

for aaaa in final1:
    final2.append(aaaa.replace(sub2, ""))

for aaa in final2:
    final3.append(aaa.replace(sub3, ""))

for bb in final3:
    final4.append(bb.replace(",", ""))

for bbb in typef:
    typef2.append(bbb.replace('.', '').strip())

for ccc in compound:
    if "Compounds" in ccc:
        compound2.append("Compound")
    else:
        compound2.append("")

for i in range(len(arr1)):

    if "Floor" in arr1[i]:
        if f == ppm:
            f += 1
            F.append(final4[i])
        else:
            f += 2
            F.append("")
            F.append(final4[i])

    elif "Room" in arr1[i]:
        if r == ppm:
            r += 1
            R.append(final4[i])
        else:
            r += 2
            R.append("")
            R.append(final4[i])

    elif "Baths" in arr1[i]:
        if b == ppm:
            b += 1
            B.append(final4[i])
        else:
            b += 2
            B.append("")
            B.append(final4[i])

    elif "Finish" in arr1[i]:
        if fi == ppm:
            fi += 1
            Fi.append(final4[i])
        else:
            fi += 2
            Fi.append("")
            Fi.append(final4[i])

    elif "Listing" in arr1[i]:
        if l == ppm:
            l += 1
            L.append(final4[i])
        else:
            l += 2
            L.append("")
            L.append(final4[i])

    elif "Price Per Meter" in arr1[i]:
        ppm += 1
        PPM.append(final4[i])

    elif "Price" in arr1[i]:
        if p == ppm:
            p += 1
            P.append(final4[i])
        else:
            p += 2
            P.append("")
            P.append(final4[i])

    elif "Built" in arr1[i]:
        if bu == ppm:
            bu += 1
            Bu.append(final4[i])
        else:
            bu += 2
            Bu.append("")
            Bu.append(final4[i])

    elif "View" in arr1[i]:
        if v == ppm:
            v += 1
            V.append(final4[i])
        else:
            v += 2
            V.append("")
            V.append(final4[i])

    elif "Size" in arr1[i]:
        if s == ppm:
            s += 1
            S.append(final4[i])
        else:
            s += 2
            S.append("")
            S.append(final4[i])

    elif "Seller" in arr1[i]:
        if se == ppm:
            se += 1
            Se.append(final4[i])
        else:
            se += 2
            Se.append("")
            Se.append(final4[i])

    elif "Payment" in arr1[i]:
        if pa == ppm:
            pa += 1
            Pa.append(final4[i])
        else:
            pa += 2
            Pa.append("")
            Pa.append(final4[i])

    elif "Mortgage" in arr1[i]:
        if m == ppm:
            m += 1
            M.append(final4[i])
        else:
            m += 2
            M.append("")
            M.append(final4[i])

    elif "Publish" in arr1[i]:
        if pu == ppm:
            pu += 1
            Pu.append(final4[i])
        else:
            pu += 2
            Pu.append("")
            Pu.append(final4[i])

workbook = xlsxwriter.Workbook('C:\\Users\\G01-S-Admin\\Desktop\\ThesisDump28.xlsx')
worksheet = workbook.add_worksheet()

array = [F, R, B, Fi, L, PPM, P, Bu, V, S, Se, Pa, M, Pu, typef2, address, compound2]

row = 0

for col, data in enumerate(array):
    worksheet.write_column(row, col, data)

workbook.close()
