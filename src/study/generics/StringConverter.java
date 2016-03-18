package study.generics;

import java.nio.ByteBuffer;

public class StringConverter implements Converter<String> {
    @Override
    public boolean transform(String src, ByteBuffer dest) {
        dest.put(src.getBytes());
        return false;
    }
}
