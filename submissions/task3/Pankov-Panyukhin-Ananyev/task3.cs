using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace ApplePen
{
    struct ProductCounter
    {
        public int appleCount;
        public int penCount;
        public ProductCounter(int appleCount = 0, int penCount = 0)
        {
            this.appleCount = appleCount;
            this.penCount = penCount;
        }

        public void AddCount(ProductCounter prod)
        {
            this.appleCount += prod.appleCount;
            this.penCount += prod.penCount;
        }

        public void SubstractCount(ProductCounter prod)
        {
            this.appleCount -= prod.appleCount;
            this.penCount -= prod.penCount;
        }
    }

    class Program
    {
        static void ReadSupplyOrInventory(string filename, ref SortedDictionary<DateTime, ProductCounter> list)
        {
            list.Clear();
            StreamReader reader = new StreamReader(filename);
            reader.ReadLine();
            while (!reader.EndOfStream)
            {
                var str = reader.ReadLine();
                var spl = str.Split(',');
                if (spl.Length == 3)
                {
                    DateTime date = DateTime.Parse(spl[0]);
                    list[date] = new ProductCounter(Int32.Parse(spl[1]), Int32.Parse(spl[2]));
                }
            }
            reader.Close();
        }

        static void Parse(string name, ref Dictionary<DateTime, ProductCounter> state, ref Dictionary<DateTime, ProductCounter> stolen, ref Dictionary<DateTime, ProductCounter> sell)
        {
            var supply = new SortedDictionary<DateTime, ProductCounter>();
            var inventory = new SortedDictionary<DateTime, ProductCounter>();

            ReadSupplyOrInventory(string.Format("input\\{0}-supply.csv", name), ref supply);
            ReadSupplyOrInventory(string.Format("input\\{0}-inventory.csv", name), ref inventory);

            StreamReader reader = new StreamReader(string.Format("input\\{0}-sell.csv", name));

            reader.ReadLine();

            sell.Clear();

            while (!reader.EndOfStream)
            {
                var str = reader.ReadLine();
                var spl = str.Split(',');
                if (spl.Length == 2)
                {
                    var date = DateTime.Parse(spl[0]);

                    var spl1 = spl[1].Split('-');
                    if (spl1.Length == 8)
                    {
                        var sprod = spl1[2];
                        ProductCounter toadd = new ProductCounter();
                        if (sprod == "ap")
                            toadd.appleCount = 1;
                        else if (sprod == "pe")
                            toadd.penCount = 1;

                        if (sell.ContainsKey(date))
                        {
                            var prodCount = sell[date];
                            prodCount.AddCount(toadd);
                            sell[date] = prodCount;
                        }
                        else
                            sell[date] = toadd;
                    }
                }
            }

            reader.Close();

            var firstInvDate = inventory.First().Key;
            inventory[firstInvDate.Subtract(new TimeSpan(DateTime.DaysInMonth(firstInvDate.Year, firstInvDate.Month), 0, 0, 0))] =
                new ProductCounter();

            state.Clear();
            stolen.Clear();

            bool islast = false;

            foreach (var pair in inventory)
            {
                if (islast)
                    break;
                ProductCounter counter = pair.Value;
                for (int i = 1; i <= 31; i++)
                {
                    DateTime curDate = pair.Key.Add(new TimeSpan(i, 0, 0, 0));
                    if (sell.ContainsKey(curDate))
                        counter.SubstractCount(sell[curDate]);
                    if (supply.ContainsKey(curDate))
                        counter.AddCount(supply[curDate]);
                    state[curDate] = counter;
                    DateTime nextDate = pair.Key.Add(new TimeSpan(i + 1, 0, 0, 0));
                    if (nextDate.Month != curDate.Month)
                    {
                        if (inventory.Last().Key == curDate)
                            islast = true;

                        if (inventory.ContainsKey(curDate))
                        {
                            state[curDate] = inventory[curDate];
                            var data = inventory[curDate];
                            counter.SubstractCount(data);
                            stolen[curDate] = counter;
                        }
                        break;
                    }
                }
            }
            
        }

        static void SaveCSV(string filename, ref Dictionary<DateTime, ProductCounter> data)
        {
            List<string> l = new List<string>();
            l.Add("date,apple,pen");
            l.AddRange(from x in data select x.Key.ToString("yyyy-MM-dd") + "," + x.Value.appleCount.ToString() + "," + x.Value.penCount.ToString());
            File.WriteAllLines(filename, l.ToArray());
        }
        
        struct TotalStruct
        {
            public int appleStolen;
            public int penStolen;
            public int appleSold;
            public int penSold;
        }

        static void Main(string[] args)
        {
            var filelist = Directory.GetFiles("input");
            var groupedFiles = new Dictionary<string, int>();

            foreach(var file in filelist)
            {
                var file1 = new FileInfo(file).Name.Replace(".csv", "");
                var spl = file1.Split('-');
                if (spl.Length == 3)
                {
                    var name = spl[0] + "-" + spl[1];
                    var type = spl[2];
                    var btype = 0;
                    if (groupedFiles.ContainsKey(name))
                        btype = groupedFiles[name];
                    if (type == "inventory")
                        btype = btype | 1;
                    else if (type == "supply")
                        btype = btype | 2;
                    else if (type == "sell")
                        btype = btype | 4;
                    groupedFiles[name] = btype;
                }
            }

            var daily = new Dictionary<DateTime, ProductCounter>();
            var stolen = new Dictionary<DateTime, ProductCounter>();
            var sell = new Dictionary<DateTime, ProductCounter>();

            if (!Directory.Exists("answer"))
                Directory.CreateDirectory("answer");

            var fileSummary = new Dictionary<string, TotalStruct>();
           
            foreach (var p in groupedFiles)
            {
                if (p.Value == 7) //Если есть все три файла (*inventory, *supply, *sell)
                {
                    var state = "";
                    var spl = p.Key.Split('-');
                    if (spl.Length > 0)
                        state = spl[0];

                    Parse(p.Key, ref daily, ref stolen, ref sell);
                    SaveCSV("answer\\" + p.Key + "-daily.csv", ref daily);
                    SaveCSV("answer\\" + p.Key + "-steal.csv", ref stolen);
                    
                    //Теперь агрегированные данные по штатам и годам
                    foreach(var ps in sell)
                    {
                        var yearstate = ps.Key.Year.ToString() + "," + state;
                        if (fileSummary.ContainsKey(yearstate))
                        {
                            var totalstr = fileSummary[yearstate];
                            totalstr.appleSold += ps.Value.appleCount;
                            totalstr.penSold += ps.Value.penCount;
                            fileSummary[yearstate] = totalstr;
                        }
                        else
                            fileSummary[yearstate] = new TotalStruct() { appleSold = ps.Value.appleCount, appleStolen = 0, penSold = ps.Value.penCount, penStolen = 0 };
                    }
                    foreach (var ps in stolen)
                    {
                        var yearstate = ps.Key.Year.ToString() + "," + state;
                        if (fileSummary.ContainsKey(yearstate))
                        {
                            var totalstr = fileSummary[yearstate];
                            totalstr.appleStolen += ps.Value.appleCount;
                            totalstr.penStolen += ps.Value.penCount;
                            fileSummary[yearstate] = totalstr;
                        }
                        else
                            fileSummary[yearstate] = new TotalStruct() { appleStolen = ps.Value.appleCount, appleSold = 0, penStolen = ps.Value.penCount, penSold = 0 };
                    }
                }
            }

            var l = new List<string>();
            l.Add("year,state,apple_sold,apple_stolen,pen_sold,pen_stolen");
            l.AddRange(from x in fileSummary select x.Key + "," + x.Value.appleSold.ToString() + "," + x.Value.appleStolen.ToString() 
                       + "," + x.Value.penSold.ToString() + "," + x.Value.penStolen.ToString());
            File.WriteAllLines("answer\\sold_stolen_stat.csv", l.ToArray());
        }
    }
}
