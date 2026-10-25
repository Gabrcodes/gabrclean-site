"""Generate en/index.html from the Arabic index.html.

The Arabic page is the source of truth. Every replacement must match exactly
once or more; a miss stops the build so a stale translation never ships.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).parent
AR = ROOT / "index.html"
EN = ROOT / "en" / "index.html"

WA_AR = "?text=%D8%A3%D9%87%D9%84%D8%A7%D9%8B%20%D8%AC%D8%A8%D8%B1%20%D9%83%D9%84%D9%8A%D9%86%D8%8C%20%D8%B9%D8%A7%D9%8A%D8%B2%20%D8%A3%D8%AD%D8%AC%D8%B2"
WA_EN = "?text=Hi%20Gabrclean%2C%20I%27d%20like%20to%20book"

PAIRS = [
    ('<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">'),
    ("<title>جبر كلين | دراي كلين في المعادي من 1987</title>", "<title>Gabrclean | Dry cleaning in Maadi since 1987</title>"),
    ('content="جبر كلين، دراي كلين في المعادي من 1987: دراي كلين، غسيل ومكوى، صباغة هدوم بالأسود والبني والكحلي، وتنضيف سجاد في البيت. استلام وتسليم في كل القاهرة."',
     'content="Gabrclean, a Maadi dry cleaner since 1987: dry cleaning, washing and ironing, garment dyeing in black, brown and navy, and on-site carpet cleaning. Pickup and delivery across Cairo."'),
    ('content="دراي كلين · غسيل ومكوى · صباغة هدوم · سجاد. استلام وتسليم في كل القاهرة."', 'content="Dry cleaning · Washing &amp; ironing · Garment dyeing · Carpets. Pickup and delivery across Cairo."'),
    ('<meta property="og:url" content="https://clean.gabr.online/">', '<meta property="og:url" content="https://clean.gabr.online/en/">'),
    ('href="assets/', 'href="../assets/'),
    ('src="assets/', 'src="../assets/'),
    ('aria-label="أقسام الموقع"', 'aria-label="Sections"'),
    ('<a href="#services">خدماتنا</a><a href="#how">إزاي بنشتغل</a><a href="#signature">سيجنتشر</a><a href="#visit">المكان والمواعيد</a>',
     '<a href="#services">Services</a><a href="#how">How it works</a><a href="#signature">Signature</a><a href="#visit">Visit</a>'),
    ('<a class="lang" href="en/" hreflang="en" lang="en">English</a>', '<a class="lang" href="../" hreflang="ar" lang="ar">العربية</a>'),
    (WA_AR, WA_EN),
    ("احجز على واتساب", "Book on WhatsApp"),
    ("<h1>دراي كلين في المعادي<br><em>من سنة 1987</em></h1>", "<h1>Dry cleaning in Maadi<br><em>since 1987</em></h1>"),
    ('<p class="lead">بنستلم هدومك من أي مكان في القاهرة، وترجعلك نضيفة ومكوية ومتغلفة. ومعاها صباغة الهدوم الباهتة وتنضيف السجاد في البيت.</p>',
     '<p class="lead">We pick up your clothes anywhere in Cairo and bring them back clean, pressed and wrapped. We also dye faded clothes back to color and clean carpets at home.</p>'),
    ('اتصل بينا <span class="num">', 'Call us <span class="num">'),
    ("<span>على نفس الشارع</span>", "<span>On the same street</span>"),
    ("<b>كل القاهرة</b><span>استلام وتسليم</span>", "<b>All Cairo</b><span>Pickup &amp; delivery</span>"),
    ("<span>تقييم جوجل</span>", "<span>Google rating</span>"),
    ('<p>شارع عبد المنعم رياض، المعادي.<br><span class="en">Same street, same name.</span></p>', '<p>Abdel Moneim Riad St., Maadi.<br>Same street, same name.</p>'),
    ("<h2>خدماتنا</h2>", "<h2>Our services</h2>"),
    ("<p>من 1987 وإحنا بنعتني بهدوم أهل المعادي، ودلوقتي كل القاهرة.</p>", "<p>Caring for Maadi's clothes since 1987, and now all of Cairo's.</p>"),
    ('<h3>دراي كلين</h3><span class="en">Dry cleaning</span>', '<h3>Dry cleaning</h3><span class="sub" lang="ar">دراي كلين</span>'),
    ("<p>بدل، فساتين، جواكت، وكل قطعة محتاجة عناية خاصة.</p>", "<p>Suits, dresses, jackets and anything that needs special care.</p>"),
    ('<h3>غسيل ومكوى</h3><span class="en">Washing &amp; ironing</span>', '<h3>Washing &amp; ironing</h3><span class="sub" lang="ar">غسيل ومكوى</span>'),
    ("<p>قمصان وهدوم يومية، مغسولة ومكوية وجاهزة تتلبس.</p>", "<p>Shirts and everyday clothes, washed, pressed and ready to wear.</p>"),
    ('<span class="badge">تخصصنا</span>', '<span class="badge">Our specialty</span>'),
    ('<h3>صباغة هدوم</h3><span class="en">Garment dyeing</span>', '<h3>Garment dyeing</h3><span class="sub" lang="ar">صباغة هدوم</span>'),
    ("<p>العباية السودا بهتت؟ بنرجّع لون الهدوم الباهتة من تاني.</p>", "<p>Black abaya gone grey? We bring faded clothes back to their color.</p>"),
    ('aria-label="أسود، بني، كحلي"', 'aria-label="Black, brown, navy"'),
    ('<h3>سجاد وموكيت</h3><span class="en">Carpet cleaning</span>', '<h3>Carpet cleaning</h3><span class="sub" lang="ar">سجاد وموكيت</span>'),
    ("<p>فريقنا بييجي لحد عندك وينضف السجاد والموكيت في البيت.</p>", "<p>Our team comes to you and cleans rugs and fitted carpet at home.</p>"),
    ("<h2>إزاي بنشتغل</h2>", "<h2>How it works</h2>"),
    ("<p>من غير ما تتحرك من مكانك.</p>", "<p>Without leaving your seat.</p>"),
    ("<h3>ابعتلنا على واتساب</h3><p>قولنا عندك إيه وفين، وهنتفق على ميعاد الاستلام.</p>",
     "<h3>Message us on WhatsApp</h3><p>Tell us what you have and where, and we agree on a pickup time.</p>"),
    ("<h3>بنستلم من عندك</h3><p>المندوب بيجيلك في أي مكان في القاهرة، أو عدّي علينا في المعادي.</p>",
     "<h3>We pick up</h3><p>Our courier comes to you anywhere in Cairo, or you can drop by the shop in Maadi.</p>"),
    ("<h3>ترجعلك جاهزة</h3><p>نضيفة ومكوية ومتغلفة على الشماعة، لحد باب البيت.</p>",
     "<h3>Back to you, ready</h3><p>Clean, pressed and wrapped on a hanger, delivered to your door.</p>"),
    ('alt="يافطة جبر كلين النحاس على واجهة المحل في المعادي"', 'alt="The original brass Gabrclean sign over the shop in Maadi"'),
    ("<figcaption>اليافطة الأصلية، لسه على باب المحل.</figcaption>", "<figcaption>The original sign, still over the door.</figcaption>"),
    ("<h2>نفس الشارع، نفس الاسم، من 1987</h2>", "<h2>Same street, same name, since 1987</h2>"),
    ("<p>جبر كلين بدأ في شارع عبد المنعم رياض في المعادي سنة 1987، وفضل هناك من ساعتها. أجيال من أهل المعادي عدّوا علينا، واسمنا لسه معلّق بالنحاس فوق الباب.</p>",
     "<p>Gabrclean opened on Abdel Moneim Riad Street in Maadi in 1987 and has been there ever since. Generations of Maadi families have come through our door, and our name still hangs in brass above it.</p>"),
    ("<p>اللوجو الجديد متاخد من نفس اليافطة دي، بنفس الحروف والنُقط، بس بشكل يناسب النهارده.</p>",
     "<p>Our new logo is drawn from that same sign, with the same letters and dots, updated for today.</p>"),
    ("<h2>جبر كلين سيجنتشر</h2>", "<h2>Gabrclean Signature</h2>"),
    ("<p>للسفارات وبيوت الدبلوماسيين والشخصيات العامة: خدمة بموعد مسبق، بتعامل خاص مع كل قطعة.</p>",
     "<p>For embassies, diplomatic residences and private clients: service by appointment, with personal care for every piece.</p>"),
    ('<p class="en" style="text-align:right">For embassies, diplomatic residences and private clients: by appointment.</p>',
     '<p lang="ar">للسفارات والدبلوماسيين والشخصيات العامة، بموعد مسبق.</p>'),
    ("اطلب موعد</a>", "Request an appointment</a>"),
    ("<li>بدل، فساتين سهرة، حرير وكشمير وقطع حساسة.</li>", "<li>Suits, evening dresses, silk, cashmere and other delicate pieces.</li>"),
    ("<li>استلام وتسليم بموعد يناسبك، في أي مكان في القاهرة.</li>", "<li>Pickup and delivery at a time that suits you, anywhere in Cairo.</li>"),
    ("<li>تعامل هادي ومحترم مع بيتك ومع هدومك.</li>", "<li>Quiet, respectful handling of your home and your clothes.</li>"),
    ("<h2>المكان والمواعيد</h2>", "<h2>Visit us</h2>"),
    ("<h3>العنوان</h3>", "<h3>Address</h3>"),
    ("<p>3 شارع عبد المنعم رياض، العرب، المعادي، جنب محمصات أبو برين.</p>", "<p>3 Abdel Moneim Riad St., El Arab, Maadi, next to Abu Barrein Roastery.</p>"),
    ("افتح على الخريطة ←", "Open in Maps →"),
    ("<h3>المواعيد</h3>", "<h3>Hours</h3>"),
    ("<td>السبت – الخميس</td>", "<td>Saturday – Thursday</td>"),
    ("<td>الجمعة</td><td>إجازة</td>", "<td>Friday</td><td>Closed</td>"),
    ("<h3>تواصل معانا</h3>", "<h3>Contact</h3>"),
    ("<p>واتساب: ", "<p>WhatsApp: "),
    ("<p>تليفون: ", "<p>Phone: "),
    ("<p>إنستجرام: ", "<p>Instagram: "),
    ("<h2>هدومك تستاهل نضافة تليق بيها</h2>", "<h2>Your clothes deserve proper care</h2>"),
    ("<p>ابعتلنا دلوقتي ونحدد ميعاد الاستلام.</p>", "<p>Message us now and we'll set a pickup time.</p>"),
    ('جبر كلين · <span class="en">Gabrclean, Maadi, Cairo</span>', 'Gabrclean · <span lang="ar">جبر كلين، المعادي، القاهرة</span>'),
    ('aria-label="واتساب"', 'aria-label="WhatsApp"'),
    ('<link rel="canonical" href="https://clean.gabr.online/">', '<link rel="canonical" href="https://clean.gabr.online/en/">'),
    ("<p>إيميل: ", "<p>Email: "),
    ("<h2>أسئلة بتتسأل كتير</h2>", "<h2>Frequently asked questions</h2>"),
    ("بتستلموا الهدوم من فين؟", "Where do you pick up from?"),
    ("من أي مكان في القاهرة: المعادي، الزمالك، مصر الجديدة، التجمع، مدينة نصر وغيرها. ابعتلنا على واتساب ونتفق على ميعاد الاستلام.",
     "Anywhere in Cairo: Maadi, Zamalek, Heliopolis, New Cairo, Nasr City and more. Message us on WhatsApp and we'll agree on a pickup time."),
    ("بتصبغوا الهدوم بألوان إيه؟", "Which colors do you dye clothes in?"),
    ("بنصبغ بالأسود والبني والكحلي، وده بيرجّع لون الهدوم الباهتة زي العبايات والبناطيل والبدل. ابعتلنا صورة القطعة ونقولك ينفع ولا لأ.",
     "Black, brown and navy. It brings faded clothes such as abayas, trousers and suits back to their color. Send us a photo and we'll tell you if it can be done."),
    ("بتنضفوا السجاد في البيت؟", "Do you clean carpets at home?"),
    ("أيوه، فريقنا بييجي لحد عندك وينضف السجاد والموكيت في البيت.", "Yes. Our team comes to you and cleans rugs and fitted carpet in your home."),
    ("مواعيدكم إيه؟", "What are your opening hours?"),
    ("مفتوحين من 10 الصبح لـ 10 بالليل من السبت للخميس، والجمعة إجازة.", "We're open 10 am to 10 pm, Saturday to Thursday. Closed on Fridays."),
]


def main():
    s = AR.read_text(encoding="utf-8")
    missing = [a for a, _ in PAIRS if a not in s]
    if missing:
        sys.exit("Arabic source changed; update these pairs:\n" + "\n".join(m[:90] for m in missing))
    for a, b in PAIRS:
        s = s.replace(a, b)
    EN.parent.mkdir(exist_ok=True)
    EN.write_text(s, encoding="utf-8", newline="\n")
    print(f"wrote {EN.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
