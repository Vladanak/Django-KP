var hashTags = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('q'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '/hashtag.json?q=%QUERY',
    remote: {
        url: '/hashtag.json?q=%QUERY',
        wildcard: '%QUERY'
    }
});

$('#typehead'.typehead)(null,{
    name: 'hashTag',
    displayKey: 'q',
    source: hashTags.ttAdapter()
});