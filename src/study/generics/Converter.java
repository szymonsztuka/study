package study.generics;

import java.nio.ByteBuffer;

public interface Converter<T> {
    boolean transform(T src, ByteBuffer dest);
}
