import os
import json
import sys
from firecrawl import Firecrawl
from dotenv import load_dotenv


load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.text_cleaner import clean_text, is_meaningful
firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

URLS = [
    "https://www.bis.gov.in/?lang=en",
    "https://www.bis.gov.in/product-certification/?lang=en",
    "https://www.bis.gov.in/conformity-assessment/?lang=en",
    "https://www.bis.gov.in/standards/?lang=en",
    "https://www.bis.gov.in/consumer-overview/?lang=en",
    "https://www.bis.gov.in/about-bis/?lang=en",
    "https://www.bis.gov.in/hallmarking/?lang=en",
    "https://www.bis.gov.in/laboratory-services/?lang=en",
    "https://www.bis.gov.in/press-releases/?lang=en",
    "https://www.bis.gov.in/publications/?lang=en",
    "https://www.bis.gov.in/annual-reports/?lang=en",
]

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "bis_pages.json"
)

def scrape_all():
    results = []

    for url in URLS:
        try:
            print(f"Scraping: {url}")
            response = firecrawl.scrape(url, formats=["markdown"])

            content = ""
            title = url

            if hasattr(response, "markdown"):
                content = response.markdown or ""
            if hasattr(response, "metadata") and response.metadata:
                title = getattr(response.metadata, "title", url) or url

            # Clean the text
            content = clean_text(content)

            # Check if meaningful English content
            if is_meaningful(content):
                results.append({
                    "title": title,
                    "content": content,
                    "source": url.replace("?lang=en", "")
                })
                print(f"  Got {len(content)} chars")
            else:
                print(f"  Skipped (not enough English content)")

        except Exception as e:
            print(f"  Error: {e}")

    return results


def get_manual_data():
    return [
        {
            "title": "About BIS - Bureau of Indian Standards",
            "content": "The Bureau of Indian Standards (BIS) is the National Standards Body of India working under the Ministry of Consumer Affairs, Food and Public Distribution, Government of India. It is established by the Bureau of Indian Standards Act 2016. BIS has been providing traceability and tangibility to standardization, certification and testing activities. Core functions include: Standards Formulation, Product Certification, Hallmarking of Gold and Silver Jewellery, Laboratory Services, Training Services and Consumer Affairs.",
            "source": "https://www.bis.gov.in/about-bis/"
        },
        {
            "title": "BIS Product Certification and ISI Mark",
            "content": "BIS Product Certification scheme certifies that a product conforms to a specific Indian Standard. The ISI Mark is the most popular certification mark in India. Products can be certified voluntarily or mandatorily. Mandatory certification covers products affecting health and safety such as electrical appliances, cement, steel, LPG cylinders, helmets, and food products. The ISI mark guarantees quality, safety and reliability of products.",
            "source": "https://www.bis.gov.in/product-certification/"
        },
        {
            "title": "How to Apply for BIS Certification",
            "content": "Steps to apply for BIS certification: 1) Visit manakonline.in portal and register as manufacturer. 2) Select applicable Indian Standard for your product. 3) Fill application form and upload documents including factory details and equipment list. 4) Pay application and marking fees. 5) BIS officer visits factory for inspection. 6) Product samples sent to recognized laboratory for testing. 7) If tests pass, BIS license is issued allowing use of ISI mark on the product.",
            "source": "https://www.bis.gov.in/product-certification/"
        },
        {
            "title": "BIS Hallmarking for Gold and Silver Jewellery",
            "content": "BIS Hallmarking is a quality certification of precious metal articles in India. Hallmarking of gold jewellery is mandatory in India. The BIS hallmark consists of BIS logo, purity grade such as 916 for 22 karat gold, and a unique HUID number. Consumers can verify hallmark genuineness using the BIS Care app. Jewellers need a BIS licence to sell hallmarked jewellery. Hallmarking ensures consumers get correct purity of gold and silver.",
            "source": "https://www.bis.gov.in/hallmarking/"
        },
        {
            "title": "BIS Standards Formulation",
            "content": "BIS formulates Indian Standards through a consultative process involving industry, consumers, scientific institutions and government. There are more than 20000 Indian Standards in force covering food, agriculture, chemicals, civil engineering, electrical, electronics, mechanical, metallurgical, medical equipment and textiles. Standards can be purchased from the BIS website at bis.gov.in or standardsbis.in.",
            "source": "https://www.bis.gov.in/standards/"
        },
        {
            "title": "BIS Laboratory Services",
            "content": "BIS has a network of NABL accredited laboratories to support certification and testing activities. Services include testing of products for certification, calibration services, and training. BIS maintains a list of recognized laboratories across India for product testing. Lab fees and list of recognized labs are available at crsbis.in.",
            "source": "https://www.bis.gov.in/laboratory-services/"
        },
        {
            "title": "BIS Consumer Awareness and Complaints",
            "content": "BIS runs consumer awareness programmes to educate people about standardization and quality. Consumers can report fake ISI mark products via BIS Care mobile app, the bis.gov.in portal, or any BIS regional or branch office. BIS conducts raids and takes legal action against manufacturers misusing the ISI mark. BIS organizes consumer connect programmes across India.",
            "source": "https://www.bis.gov.in/consumer-overview/"
        },
        {
            "title": "BIS Conformity Assessment Schemes",
            "content": "BIS conformity assessment schemes include: 1) Product Certification Scheme with ISI Mark for industrial products. 2) Compulsory Registration Scheme (CRS) for electronics and IT products like mobile phones, laptops, LED lights and power banks. 3) Foreign Manufacturers Certification Scheme (FMCS) for imported products. 4) Management System Certification for ISO standards. 5) Hallmarking Scheme for gold and silver jewellery. 6) Eco Mark Scheme for environment friendly products.",
            "source": "https://www.bis.gov.in/conformity-assessment/"
        },
        {
            "title": "BIS International Relations",
            "content": "BIS represents India in international and regional standards bodies including ISO (International Organization for Standardization) and IEC (International Electrotechnical Commission). BIS has signed MoUs with national standards bodies of several countries for mutual cooperation. BIS participates in Pacific Area Standards Congress (PASC) and South Asian Regional Standards Organization (SARSO). International cooperation helps align Indian Standards with global standards.",
            "source": "https://www.bis.gov.in/about-bis/"
        },
        {
            "title": "BIS Legislation and Legal Framework",
            "content": "BIS is established under the Bureau of Indian Standards Act 2016 which replaced the BIS Act 1986. The Act empowers the government to make certification of any article compulsory. The BIS Conformity Assessment Regulations 2018 govern the certification process. Misuse of BIS certification marks is a punishable offence under the Act. BIS can conduct raids and take legal action against violators.",
            "source": "https://www.bis.gov.in/about-bis/"
        },
        {
            "title": "BIS Certification Fees and Charges",
            "content": "BIS certification fees include: non-refundable application fee, Annual Minimum Marking Fee (AMMF), and marking fee based on production quantity. Fee structure varies by product category and Indian Standard. Testing charges are separate and paid to the testing laboratory. For exact fee details visit manakonline.in or contact nearest BIS regional or branch office. Foreign manufacturers under FMCS scheme pay additional fees.",
            "source": "https://www.bis.gov.in/product-certification/"
        },
        {
            "title": "BIS Grievance Redressal System",
            "content": "Consumers can file complaints against fake BIS certified products via: BIS Care mobile app, consumer portal on bis.gov.in, or any BIS regional or branch office. BIS has regional offices across India to handle complaints. Enforcement actions include raids, seizures and legal proceedings against violators. For grievances related to BIS services, complaints can be filed online at bis.gov.in.",
            "source": "https://www.bis.gov.in/consumer-overview/"
        },
        {
            "title": "BIS Publications and Annual Reports",
            "content": "BIS publishes annual reports, Indian Standards, technical guides and consumer awareness materials. Annual reports from 2011 to 2021 are available on the BIS website. BIS publishes the Indian Standards catalogue. Standards can be purchased online from bis.gov.in. BIS also publishes handbooks and special publications for various sectors. Press releases and news updates are regularly published on the BIS website.",
            "source": "https://www.bis.gov.in/"
        },
        {
            "title": "BIS Compulsory Registration Scheme for Electronics",
            "content": "The Compulsory Registration Scheme (CRS) under BIS makes it mandatory for electronics and IT products to be registered before sale in India. Products covered include mobile phones, laptops, tablets, LED lights, power banks, smart watches, printers and more. Foreign manufacturers must appoint an Authorized Indian Representative (AIR) to register their products. CRS ensures electronics sold in India meet Indian safety standards.",
            "source": "https://www.bis.gov.in/conformity-assessment/"
        },
        {
            "title": "BIS Foreign Manufacturers Certification Scheme",
            "content": "The Foreign Manufacturers Certification Scheme (FMCS) allows foreign manufacturers to obtain BIS certification for products exported to India. The foreign manufacturer applies through an Authorized Indian Representative (AIR). BIS conducts factory inspection abroad. Products must conform to relevant Indian Standards. FMCS ensures imported products meet the same quality standards as domestically manufactured products.",
            "source": "https://www.bis.gov.in/conformity-assessment/"
        },
    ]


def main():
    print("\nStarting BIS scraping with Firecrawl...\n")
    scraped_data = scrape_all()

    print(f"\nScraped {len(scraped_data)} pages from BIS website.")
    print("Merging with curated knowledge base...\n")

    manual_data = get_manual_data()

    # Combine scraped + manual
    combined = scraped_data + manual_data

    # Deduplicate by source — keep longer content
    seen_sources = {}
    final_data = []
    for item in combined:
        src = item["source"]
        if src not in seen_sources:
            seen_sources[src] = len(final_data)
            final_data.append(item)
        else:
            existing_idx = seen_sources[src]
            if len(item["content"]) > len(final_data[existing_idx]["content"]):
                final_data[existing_idx] = item

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(final_data)} total entries.")
    print(f"  - {len(scraped_data)} from live BIS website scraping")
    print(f"  - {len(manual_data)} from curated BIS knowledge base")


if __name__ == "__main__":
    main()