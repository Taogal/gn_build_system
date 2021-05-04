// Copyright 2014 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include <stdio.h>

#include "../src/hello_static.h"
#include "../src/hello_shared.h"

int main(int argc, char* argv[]) {
  printf("%s %s\n", GetStaticText(),GetSharedText());
  return 0;
}
