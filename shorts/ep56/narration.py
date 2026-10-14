# 場面ごとのナレーションを生成(edge-tts / ja-JP-NanamiNeural)。 python3 narration.py
import certifi, asyncio, json, subprocess
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'  # プロキシのCAを使う
import edge_tts
LINES = [
 "第56話。お客様ゼロなのに、パートを4人採用した理由。",
 "お客様ゼロ。売上ゼロ。なのに、パートスタッフを4人採用しました。",
 "普通は、売上が増えてから人を雇う。でも私は逆。理想の体制を、先につくろうと考えました。",
 "税理士事務所の仕事の、95パーセントは事務作業。でも私が経営者と考えたいのは、会社の未来です。",
 "独立するとき、決めました。自分では、入力作業を一切しない。数字はスタッフに任せ、私は経営者と話をする。",
 "事務所は、郊外の住宅地に。求人には、遅刻・早退OK、と書きました。働きやすさを、大切にしたのです。",
 "すると、応募がたくさん。一番最初の方は、なんと税理士の有資格者。今も、活躍してくれています。",
 "お客様とのやり取りは、LINEが中心。資料の確認や不明点は、グループの中で完結させます。",
 "せっかく社長と会うのに、支払いの確認ばかりではもったいない。社長、これからどうしましょうか。その話をしたいのです。",
 "私ひとりではできません。スタッフが正確に数字をつくってくれるから、経営の話に集中できるのです。",
 "売上を待つのではなく、理想の形を先につくり、そこへ向かって売上をつくる。未来から逆算する、経営判断でした。",
 "数字をつくる時間を減らすためではない。数字を使って、未来を考える時間を増やすために。それが、私の事務所づくりです。",
]
async def one(i, t):
    f = f'audio/s{i+1:02d}.mp3'
    await edge_tts.Communicate(t, 'ja-JP-NanamiNeural', rate='+12%').save(f)
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
    return round(d, 2)
async def main():
    durs = await asyncio.gather(*[one(i, t) for i, t in enumerate(LINES)])
    open('narr.js', 'w').write('window.NARR=' + json.dumps(durs) + ';')
    print(durs, sum(durs))
asyncio.run(main())
