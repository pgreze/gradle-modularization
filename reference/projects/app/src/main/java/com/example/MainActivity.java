package com.example;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import java.util.Arrays;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView textView = findViewById(R.id.text);
        textView.setText(
                Arrays.asList(
                        textView.getText(),
                        JavaLibrary.fct(),
                        KotlinLibraryKt.fct(),
                        JavaAndroidLibrary.afct(),
                        KotlinAndroidLibraryKt.afct()
                ).toString());
    }
}
