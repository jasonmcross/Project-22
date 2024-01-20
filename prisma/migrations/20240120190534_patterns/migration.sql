/*
  Warnings:

  - A unique constraint covering the columns `[name]` on the table `patterns` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "patterns_name_key" ON "patterns"("name");
