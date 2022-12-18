import requests
from bs4 import BeautifulSoup
import re
import pymssql

conn = pymssql.connect("Databse Server", "Database User Name", "Database password", "Database Name")
cursor = conn.cursor()
sql = "truncate table GraphicCards"
cursor.execute(sql)
conn.commit()

pattern = '<[^<]+?>'
reqs = requests.get("https://hashrate.no")
soup = BeautifulSoup(reqs.text, 'html.parser')
Links = soup.find_all(
    "a", {"class": "gpulist"}, href=True)
for link in Links:
    if len(link['href']) < 8:
        reqs = requests.get("https://hashrate.no" + link['href'])
        soup = BeautifulSoup(reqs.text, 'html.parser')
        FullName = soup.find_all('title')
        FullName = re.sub(pattern, "", str(FullName))
        FullName = str(FullName).replace(" mining calculator - Hashrate.no", "").replace("[", "").replace("]", "")
        ModelName = str(link['href']).replace("/", "")
        Coins = soup.find_all(
            "div", {"class": "w3-col l8"})
        DualMiningChar = "+"
        Counter = 1
        for Coin in Coins:
            CoinDiv = Coin.find_all("div", {"class": "w3-row mainContentList"})
            for Spec in CoinDiv:
                CoinName = Spec.find_all("a", {"class": "gpulist"})
                CoinName = re.sub(pattern, "", str(CoinName))
                CoinName = CoinName.replace("[ ", "").replace("]", "")
                if DualMiningChar in CoinName:
                    CoinHashrate = Spec.find_all("td")[0]
                    CoinHashrate = re.sub(pattern, "", str(CoinHashrate))
                    CoinPerDay = Spec.find_all("td")[1]
                    CoinPerDay = re.sub(pattern, "", str(CoinPerDay))
                    CoinEfficiency = Spec.find_all("td")[2]
                    CoinEfficiency = re.sub(pattern, "", str(CoinEfficiency))
                    CoinHashrateDual = Spec.find_all("td")[6]
                    CoinHashrateDual = re.sub(pattern, "", str(CoinHashrateDual))
                    CoinRevenueDual = Spec.find_all("td")[7]
                    CoinRevenueDual = re.sub(pattern, "", str(CoinRevenueDual))
                    CoinEfficiencyDual = Spec.find_all("td")[8]
                    CoinEfficiencyDual = re.sub(pattern, "", str(CoinEfficiencyDual))
                    CoinPower = Spec.find_all("td")[12]
                    CoinPower = re.sub(pattern, "", str(CoinPower))
                    CoinRevenue = Spec.find_all("td")[13]
                    CoinRevenue = re.sub(pattern, "", str(CoinRevenue))
                    CoinProfit = Spec.find_all("td")[14]
                    CoinProfit = re.sub(pattern, "", str(CoinProfit))
                    CoinROI = Spec.find_all("td")[15]
                    CoinROI = re.sub(pattern, "", str(CoinROI))
                    CoinPower24 = Spec.find_all("td")[20]
                    CoinPower24 = re.sub(pattern, "", str(CoinPower24))
                    CoinRev24 = Spec.find_all("td")[21]
                    CoinRev24 = re.sub(pattern, "", str(CoinRev24))
                    CoinProfit24 = Spec.find_all("td")[22]
                    CoinProfit24 = re.sub(pattern, "", str(CoinProfit24))
                    CoinKwh = Spec.find_all("td")[23]
                    CoinKwh = re.sub(pattern, "", str(CoinKwh))
                else:
                    CoinHashrate = Spec.find_all("td")[0]
                    CoinHashrate = re.sub(pattern, "", str(CoinHashrate))
                    CoinPerDay = Spec.find_all("td")[1]
                    CoinPerDay = re.sub(pattern, "", str(CoinPerDay))
                    CoinEfficiency = Spec.find_all("td")[2]
                    CoinEfficiency = re.sub(pattern, "", str(CoinEfficiency))
                    CoinPower = Spec.find_all("td")[6]
                    CoinPower = re.sub(pattern, "", str(CoinPower))
                    CoinRevenue = Spec.find_all("td")[7]
                    CoinRevenue = re.sub(pattern, "", str(CoinRevenue))
                    CoinProfit = Spec.find_all("td")[8]
                    CoinProfit = re.sub(pattern, "", str(CoinProfit))
                    CoinROI = Spec.find_all("td")[9]
                    CoinROI = re.sub(pattern, "", str(CoinROI))
                    CoinPower24 = Spec.find_all("td")[14]
                    CoinPower24 = re.sub(pattern, "", str(CoinPower24))
                    CoinRev24 = Spec.find_all("td")[15]
                    CoinRev24 = re.sub(pattern, "", str(CoinRev24))
                    CoinProfit24 = Spec.find_all("td")[16]
                    CoinProfit24 = re.sub(pattern, "", str(CoinProfit24))
                    CoinKwh = Spec.find_all("td")[17]
                    CoinKwh = re.sub(pattern, "", str(CoinKwh))
                    CoinHashrateDual = "N/A"
                    CoinRevenueDual = "N/A"
                    CoinEfficiencyDual = "N/A"

                    # print(CoinKwh)
                    # print(re.sub(pattern, "", str(CoinRevenue)))
                    # CoinName = CoinDiv.find_all("a", {"class": "gpulist"}).text
                    # print(re.sub(pattern, "", str(CoinDiv))+"\n")
                    # print(str(CoinDiv))
                    #
                if Counter == 1:
                    TopCoin = True
                else:
                    TopCoin = False
                conn = pymssql.connect("Databse Server", "Database User Name", "Database password", "Database Name")
                cursor = conn.cursor()
                sql = "INSERT INTO GraphicCards (Model,Coin,Hashrate,Power,Power24H," \
                      "Efficiency,Revenue,Profit24h,ROI,ROIProfit,TopRev,FullModel," \
                      "HashrateDual,RevenueDual,EfficiencyDual) VALUES (%s,%s" \
                      ",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (ModelName, CoinName, CoinHashrate, CoinPower, CoinPower24, CoinEfficiency,
                       CoinRevenue, CoinProfit24, CoinROI, CoinProfit, TopCoin, FullName, CoinHashrateDual,
                       CoinRevenueDual, CoinEfficiencyDual)
                cursor.execute(sql, val)
                conn.commit()
                Counter = Counter + 1
