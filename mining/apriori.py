# def run_association_rule_mining(filepath):
#     import pandas as pd
#     from mlxtend.frequent_patterns import apriori, association_rules

#     df = pd.read_csv(filepath)
#     df = df.applymap(lambda x: 1 if x else 0)

#     # Step 1: Generate frequent itemsets
#     frequent_itemsets = apriori(df, min_support=0.2, use_colnames=True)

#     # 🔍 Debug output
#     print("Frequent Itemsets:")
#     print(frequent_itemsets)

#     # Step 2: Generate rules
#     rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

#     # 🔍 Debug output
#     print("Rules:")
#     print(rules)

#     if rules.empty:
#         return []

#     rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
#     rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

#     return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_dict(orient='records')

def run_association_rule_mining(filepath, min_support=0.2, min_confidence=0.6, min_threshold=1.0):
    import pandas as pd
    from mlxtend.frequent_patterns import apriori, association_rules

    df = pd.read_csv(filepath)
    df = df.applymap(lambda x: 1 if x else 0)

    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    print("Frequent Itemsets:")
    print(frequent_itemsets)

    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold)
    rules = rules[rules['confidence'] >= min_confidence]
    
    print("Rules:")
    print(rules)

    if rules.empty:
        return []

    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

    return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_dict(orient='records')
