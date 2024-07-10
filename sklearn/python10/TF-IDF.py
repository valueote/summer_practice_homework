from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == "__main__":
    corpus = [
        "我 来到 北京 清华大学",  
        "他 来到 了 网易 杭研 大厦",  
        "小明 硕士 毕业 与 中国 科学院",  
        "我 爱 北京 天安门"  
    ]
    vectorizer = CountVectorizer()  
    transformer = TfidfTransformer()  
    tfidf = transformer.fit_transform(
        vectorizer.fit_transform(corpus))  
    word = vectorizer.get_feature_names_out()  
    weight = tfidf.toarray()  
    for i in range(len(weight)):  
        print("-------这里输出第", i, "类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])