"""Audit worked examples by date with exact fractions and explicit rounding.

Run offline with Python 3. No model access or third party packages required.
"""
from fractions import Fraction as F
from math import prod
from pathlib import Path
import json

INPUT = Path(__file__).resolve().parent.parent / "data" / "teaching-cases.json"


def timeline_value(rate, amounts):
    q = 1 + F(rate)
    if q <= 0:
        raise ValueError("nonpositive accumulation factor")
    return sum(F(amount) / q ** period for period, amount in enumerate(amounts))


def balance_path(start, cash):
    amounts = []
    for movement in cash:
        start += movement
        amounts.append(start)
    return amounts


def advancing_returns(start, rates):
    return start * prod(1 + F(r) for r in rates)


def fitted_line(x, y):
    if len(x) != len(y) or len(x) < 2:
        raise ValueError("at least two matched rows required")
    mx, my = F(sum(x), len(x)), F(sum(y), len(y))
    ssx = sum((a - mx) ** 2 for a in x)
    if not ssx:
        raise ValueError("benchmark values do not vary")
    slope = sum((a - mx) * (b - my) for a,b in zip(x,y)) / ssx
    return my - slope * mx, slope


def verify(data):
    n = 0

    def equal(actual, expected):
        nonlocal n
        if actual != expected:
            raise AssertionError((n+1,actual,expected))
        n += 1

    def cents(x, shown):
        equal(round(x,2), F(shown))

    # 0–1: date-zero, contribution, and funding gap are different features.
    equal(400-360,40)
    order = data["order"]
    baseline = balance_path(0,order["cash"])
    equal(baseline,[-2400,-3600,1200])
    equal(-min(baseline),3600)
    early = balance_path(0, [order["cash"][0], order["cash"][2], order["cash"][1]])
    equal(early,[-2400,2400,1200])
    partial=order["partial_order_cash"]
    equal(balance_path(0,[-2400+partial,-1200,4800-partial]),[-1400,-2600,1200])

    # 2–3: denominators, rates and units.
    cents(F(4000,140),"28.57")
    cents(F(10000,140),"71.43")
    equal((100,40,100-40),(100,40,60))
    cents((F("1.06")/F("1.04")-1)*100,"1.92")
    cents((F("1.01")**12-1)*100,"12.68")
    equal((100*F("1.10"),100*F("1.20")),(110,120))
    cents((F("1.08")/F("1.06")-1)*100,"1.89")
    equal(F("1.08")/1-1,F(".08"))

    # 4–5: account balances and cash independently tie at two dates.
    a=data["accounting"]
    sale,paper,wages=a["reported_sale"],a["paper"],a["wages"]
    day21= sale-paper-wages
    cf=-paper-wages
    equal((day21,cf,day21-cf),(1200,-3600,4800))
    equal((sale-3000,cf+3000),(1800,-600))
    ni=day21-a["depreciation"]
    indirect=ni+a["depreciation"]-sale
    end_cash=a["starting_cash"]+cf-a["equipment"]
    ppe=a["equipment"]-a["depreciation"]
    equal((ni,indirect,end_cash,ppe),(900,cf,1400,2700))
    equal(end_cash+sale+ppe, a["starting_cash"]+ni)
    equal((end_cash+sale, end_cash+1000),(6200,2400))
    equal((cf-a["equipment"],0),(-6600,0))  # equipment mislabeled operating

    # 6: independent return on equity cross-check.
    measure=[]
    for company in ("A","B"):
        s,y,a,e,ca,cl=data["ratios"][company]
        m,t,l=F(y,s),F(s,a),F(a,e)
        equal(m*t*l,F(y,e))
        measure.append((m,t,l,F(y,e),F(ca,cl)))
    equal(measure,[(F(".08"),2,2,F(".32"),F("1.25")),(F(".06"),4,2,F(".48"),F("1.30"))])
    equal((F(250,100),F(40,100)),(F("2.5"),F(".4")))

    # 7–9: compound the discounted deposit back to its date and check residual balances.
    single=data["timelines"]["single"]
    rate=F(single["rate"]); p=single["deposit"]
    future=[p*(1+rate)**t for t in range(1,4)]
    equal(future,[1260,1323,F("1389.15")])
    equal(future[-1]/(1+rate)**2,1260)
    equal(future[-1]-p*(1+3*rate),F("9.15"))
    ann=data["timelines"]["ordinary"]
    cash=[ann["cash"]]*ann["periods"]
    v=timeline_value(ann["rate"],[0]+cash)
    early_ann=timeline_value(ann["rate"],cash)
    cents(v,"272.32")
    cents(early_ann,"285.94")
    equal(v*(1+F(ann["rate"])),early_ann)
    equal(timeline_value(0,[0]+cash),300)
    equal(F(100)/F(".05"),2000)
    cents(timeline_value(".05",[0,0]+cash),"259.36")
    loan=data["timelines"]["loan"]; ra=F(loan["rate"])
    ann_factor=timeline_value(ra,[0]+[1]*loan["periods"])
    payment=loan["principal"]/ann_factor
    outstanding=loan["principal"]
    cents(payment,"345.71")
    for year in (1,2):
        interest=outstanding*ra
        principal=payment-interest
        if year==1:
            equal(interest,60)
            cents(principal,"285.71")
        outstanding-=principal
    equal(outstanding,0)
    uneven=data["timelines"]["uneven"]
    cents(timeline_value(uneven["rate"],uneven["cash"]),"22.44")
    cents(timeline_value(uneven["rate"],[-1200,650,500,300]),"68.67")
    cents(timeline_value(uneven["rate"],[-1200,300,500,550]),"-56.95")
    equal(timeline_value(0,uneven["cash"]),250)

    # 10–11: bond price limits and cash claims under two states.
    b=data["bonds"]; c=b["coupon"]; face=b["face"]
    for years,expected in zip(b["years"],("981.31","963.84","947.51")):
        series=[0]+[c]*(years-1)+[c+face]
        cents(timeline_value(b["yield"],series),expected)
        equal(timeline_value(F(c,face),series),face)
    equal([(min(assets,160),max(assets-160,0)) for assets in (220,120)],[(160,60),(120,0)])
    equal(F(2)/(F(".08")-F(".03")),40)
    equal(5*9,45)
    cents(F(2)/(F(".09")-F(".03")),"33.33")

    # 12–15: distinguish returns in the observation record from a probability model.
    series=data["returns"]
    facts=data["reported_fund_returns"]
    rnd=series["fictional_equity"]
    equal([advancing_returns(100,rnd[:i]) for i in range(1,5)],[115,F("86.25"),F("103.50"),F("113.85")])
    cents(advancing_returns(100,series["fictional_steady"]),"112.55")
    cents(advancing_returns(100,rnd[:-1]+["-.10"]),"93.15")
    cents(advancing_returns(100,[facts[str(y)]["F"] for y in (2022,2023)]),"92.03")
    cents(advancing_returns(100,[facts[str(y)]["C"] for y in (2022,2023)]),"103.36")
    equal(F(115)/F("86.25")-1,F(1,3))
    equal(round((float(F("1.1385"))**.25 - 1)*100, 2), 3.30)
    equal(round((float(F(".99"))**.5 - 1)*100, 2), -.50)
    equal(round(float(F(".02"))**.5*100, 2), 14.14)
    equal(advancing_returns(100,["-.10",".10"]),99)
    equal(advancing_returns(100,["-.20",".25"]),100)
    equal((F("-.20")+F(".25"))/2,F(".025"))
    equal(sum(F(x)**2 for x in ["-.10",".10"]),F(".02"))
    x,y=series["regression_x_pp"],series["regression_y_pp"]
    intercept,beta=fitted_line(x,y)
    equal((intercept,beta),(1,F("1.4")))
    residuals=[b-(intercept+beta*a) for a,b in zip(x,y)]
    equal(residuals,[F("-.4"),F(".8"),F("-.8"),F(".4")])
    equal(sum(residuals),0)
    equal(fitted_line(x+[0],y+[-4]),(0,beta))
    try:
        fitted_line([4,4],[1,2])
    except ValueError:
        n += 1
    else:
        raise AssertionError("flat benchmark accepted")
    x,y=series["two_states_A_pp"],series["two_states_B_pp"]
    equal((F(sum(x),2),F(sum(y),2)),(2,2))
    equal(sum((a-2)*(b-2) for a,b in zip(x,y))/2,-80)
    equal([F(a+b,2) for a,b in zip(x,y)],[1,3])
    equal([F(".4")*a+F(".6")*b for a,b in zip(x,y)],[F("2.8"),F("1.2")])

    # 16–20: check conflicting ranks, dated shortfalls, and residual hedge exposure.
    ns,nl=timeline_value(".10",[-1000,1350]),timeline_value(".10",[-5000,6500])
    cents(ns,"227.27")
    cents(nl,"909.09")
    cents(nl-ns,"681.82")
    equal((F(1350,1000)-1,F(6500,5000)-1),(F(".35"),F(".30")))
    equal(timeline_value(".10",[-5000,5700])<ns,True)
    wacc=lambda r,t: F(".60")*F(".10")+F(".40")*F(r)*(1-F(t))
    equal((wacc(".06",".25"),wacc(".06",0),wacc(".08",".25")),(F(".078"),F(".084"),F(".084")))
    weekly=data["weekly"]
    a,b=weekly["collections"]; c,d=weekly["payments"]
    delay=weekly["delayed"]; opening=weekly["initial"]
    equal(balance_path(opening,[a-c,b-d]),[800,1400])
    equal(balance_path(opening,[a-c-delay,b-d+delay]),[400,1400])
    equal(balance_path(opening,[a-c-delay+100,b-d+delay-100]),[500,1400])
    equal(balance_path(opening,[a-c-delay+80,b-d+delay-100]),[480,1380])
    equal(weekly["minimum"]+c-opening,1500)
    equal(F(20,980),F(1,49))
    equal((1000-(980+14),1000-(980+22),25+35-20),(6,-2,40))
    equal(round(((1000/980)**(365/20)-1)*100,2),44.59)
    h=data["hedge"]; locked=h["locked"]; locked_cost=locked*F(h["locked_price"])
    spots=list(map(F,h["spot_states"]))
    equal([h["invoice"]*s for s in spots],[1070,1200])
    equal([locked_cost+(h["invoice"]-locked)*s for s in spots],[1118,1144])
    equal([locked_cost+(600-locked)*s for s in spots],[690,664])

    # Capstone: all alternatives, exact threshold and three explicit perturbations.
    z=data["assessment"]; years=z["years"]
    target=z["basket_now"]*(1+F(z["inflation"]))**years
    rr=1+F(z["savings_rate"])
    savings=z["savings_now"]*rr**years+z["savings_later"]*rr
    bond=z["bond_coupon"]*rr+z["bond_last_cash"]
    low,high=z["portfolio_cases"]; avg=F(low+high,2)
    equal((target,savings,bond,avg),(F("1081.60"),F("1131.375"),1082,1135))
    equal((low<target<high,bond-target),(True,F(".40")))
    equal((1000-z["savings_now"],1000-z["bond_price"]),(450,50))
    new_target=1000*F("1.05")**2
    equal((new_target, bond<new_target<savings),(F("1102.50"),True))
    equal(z["bond_coupon"]+z["bond_last_cash"]<target,True)
    inst=z["advance_receipt"]
    offered=balance_path(0,[-2400,inst,-1200,4800-inst])
    late=balance_path(0,[-2400,-1200,inst,4800-inst])
    equal((offered,late),([-2400,-600,-1800,1200],[-2400,-3600,-1800,1200]))
    equal((-min(offered)<=z["line_limit"]<-min(late),offered[-1]==late[-1]),(True,True))

    return n


if __name__ == "__main__":
    parameters=json.loads(INPUT.read_text(encoding="utf-8"))
    print(f"{verify(parameters)} checks passed across the Principles of Finance cases and assessment.")
