import asyncio
import json
from crawl4ai import *
async def main():
    try:
        async with AsyncWebCrawler() as crawler :
            result=await crawler.arun(
                url='https://ameriabank.am/' 
            )
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
    data= {
        "վարկ": [],
        "ավանդ": [],
        "մասնաճյուղ": []
    }
    full_text = result.markdown
    for line in full_text.split('\n'):
        line=line.strip()
        if not line or len(line) < 30:
            continue
        if "վարկ" in line:
            data["վարկ"].append(line)
        elif "ավանդ" in line:
            data["ավանդ"].append(line)
        elif "մասնաճյուղ" in line:
            data["մասնաճյուղ"].append(line)
    for key in data:
        data[key]=list(set(data[key]))
    with open("info.json", "r", encoding="utf-8") as f:
        info = json.load(f)
    for key in data:
        info["Ամերիաբանկ"][key]=data[key]
    with open("info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
if __name__=="__main__":
    asyncio.run(main())