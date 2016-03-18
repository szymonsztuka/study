package study.generics;

public class StringProducer implements Producer<String>{

    private final String obj;
    public StringProducer(String data){
        obj = data;
    }
    @Override
    public String get() {
        return obj;
    }
}
