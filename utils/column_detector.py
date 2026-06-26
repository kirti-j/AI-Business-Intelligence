COLUMN_ALIASES={
    "sales":["sales","sale","revenue","amount","sales amount","total sales","total revenue","invoice amount"],

    "profit":["profit","margin","net profit","gross profit"],

    "order_id":["order id","order","invoice id","invoice","transaction id","bill number"],

    "order_date":["order date","date","purchase date","invoice date"],

    "category":["category","product category","department"],

    "product":["product","product name","item","item name"],

    "region":["region","state","city","location"],

    "customer":["customer","customer name","client","buyer"]
}

import re
def normalize(name):
    name=name.lower()
    name=name.strip()
    name=name.replace("_"," ")
    name=re.sub(r"\s+"," ",name)
    return name

from rapidfuzz import process
def detect_columns(df):
    detected={}
    normalized_columns={
        normalize(col):col
        for col in df.columns
    }
    print("\nNormalized Columns:")
    print(normalized_columns)

    for field,aliases in COLUMN_ALIASES.items():
        best_score=0
        best_column=None

        for alias in aliases:
            match=process.extractOne(alias,normalized_columns.keys(),score_cutoff=70)

            if match:
                matched_name,score,_=match
                if score >best_score:
                    best_score=score
                    best_column=normalized_columns[matched_name]


        if best_score>=70:
            detected[field]={
                "column":best_column,
                "matched_with": matched_name,
                "confidence":round(best_score,2)
            }
        else:
            detected[field] = {
                "column": None,
                "confidence": round(best_score,2)
            }

    return detected